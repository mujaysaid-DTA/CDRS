import os
import json


def refill_routes():
    base_path = os.getcwd()
    src_path = os.path.join(base_path, 'backend', 'src')

    print("🚑 Resuscitating Routes & Controllers...\n")

    # 1. CONTROLLER (The Brain)
    controller_code = '''const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/incidents.json');

// Ensure directory exists
const dataDir = path.dirname(DATA_FILE);
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

const readData = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  const data = fs.readFileSync(DATA_FILE);
  return JSON.parse(data);
};

const writeData = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

exports.getIncidents = (req, res) => {
  try {
    const incidents = readData();
    res.json(incidents);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.createIncident = (req, res) => {
  try {
    const { type, title, description, location, severity } = req.body;
    const incidents = readData();

    const newIncident = {
      id: uuidv4(),
      type,
      title,
      description,
      severity,
      location: location || { address: 'Unknown', coordinates: [0,0] },
      status: 'pending',
      upvotes: 0,
      affectedCount: 1,
      reporter: { name: 'Anonymous', verified: false },
      createdAt: new Date().toISOString(),
      images: []
    };

    incidents.unshift(newIncident);
    writeData(incidents);

    res.status(201).json(newIncident);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};
'''

    # 2. ROUTES (The Traffic Cop)
    routes_code = '''const express = require('express');
const router = express.Router();
const { getIncidents, createIncident } = require('../controllers/incidentController');

router.get('/', getIncidents);
router.post('/', createIncident);

module.exports = router;
'''

    # Write Files
    files = {
        os.path.join(src_path, 'controllers', 'incidentController.js'): controller_code,
        os.path.join(src_path, 'routes', 'incidentRoutes.js'): routes_code
    }

    for path, content in files.items():
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Restored: {os.path.basename(path)}")
        except Exception as e:
            print(f"❌ Error writing {path}: {e}")

    # Ensure Data file exists
    data_path = os.path.join(base_path, 'backend', 'data', 'incidents.json')
    if not os.path.exists(data_path):
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, 'w') as f:
            f.write('[]')
        print("✅ Created empty data store.")


if __name__ == "__main__":
    refill_routes()