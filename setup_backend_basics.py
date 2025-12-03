import os
import json


def setup_backend():
    """
    Sets up the Node.js/Express Backend with basic Incident API
    """
    base_path = os.getcwd()
    backend_path = os.path.join(base_path, 'backend')
    src_path = os.path.join(backend_path, 'src')

    print("🚀 Initializing Backend Infrastructure...\n")

    # 1. Create Directory Structure (matching your architecture)
    dirs = [
        os.path.join(src_path, 'config'),
        os.path.join(src_path, 'controllers'),
        os.path.join(src_path, 'routes'),
        os.path.join(src_path, 'models'),
        os.path.join(src_path, 'middleware'),
        os.path.join(src_path, 'utils'),
        os.path.join(backend_path, 'data')  # For local storage
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"📁 Created directory: {d}")

    # 2. backend/package.json
    package_json = {
        "name": "disaster-response-api",
        "version": "1.0.0",
        "description": "API for Disaster Response System",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "body-parser": "^1.20.2",
            "uuid": "^9.0.0"
        },
        "devDependencies": {
            "nodemon": "^3.0.1"
        }
    }

    # 3. backend/src/server.js (Entry Point)
    server_js = '''const app = require('./app');
const dotenv = require('dotenv');

dotenv.config();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`\\n🚀 Backend Server running on port ${PORT}`);
  console.log(`🔗 API URL: http://localhost:${PORT}/api/v1`);
});
'''

    # 4. backend/src/app.js (Express Config)
    app_js = '''const express = require('express');
const cors = require('cors');
const incidentRoutes = require('./routes/incidentRoutes');

const app = express();

// Middleware
app.use(cors()); // Allow Frontend to talk to Backend
app.use(express.json()); // Parse JSON bodies

// Routes
app.use('/api/v1/incidents', incidentRoutes);

// Health Check
app.get('/', (req, res) => {
  res.send('✅ Disaster Response API is active');
});

module.exports = app;
'''

    # 5. backend/src/controllers/incidentController.js
    # Using a file-based approach for now so you don't need MongoDB/SQL yet
    incident_controller = '''const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/incidents.json');

// Helper to read data
const readData = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  const data = fs.readFileSync(DATA_FILE);
  return JSON.parse(data);
};

// Helper to write data
const writeData = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

// @desc    Get all incidents
// @route   GET /api/v1/incidents
exports.getIncidents = (req, res) => {
  try {
    const incidents = readData();
    // Simulate slight network delay
    setTimeout(() => res.json(incidents), 500);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create a new incident
// @route   POST /api/v1/incidents
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

    incidents.unshift(newIncident); // Add to top of list
    writeData(incidents);

    res.status(201).json(newIncident);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};
'''

    # 6. backend/src/routes/incidentRoutes.js
    incident_routes = '''const express = require('express');
const router = express.Router();
const { getIncidents, createIncident } = require('../controllers/incidentController');

router.get('/', getIncidents);
router.post('/', createIncident);

module.exports = router;
'''

    # 7. Create some dummy data to start with
    initial_data = [
        {
            "id": "1",
            "type": "flood",
            "severity": "critical",
            "title": "Flooding at Central Bridge",
            "description": "Water levels rising rapidly due to heavy rain.",
            "location": {"address": "Central Bridge", "coordinates": [9.0820, 7.3986]},
            "status": "verified",
            "affectedCount": 25,
            "upvotes": 10,
            "reporter": {"name": "System Admin", "verified": true},
            "createdAt": "2023-10-27T10:00:00.000Z",
            "images": []
        }
    ]

    # Write Files
    file_map = {
        os.path.join(backend_path, 'package.json'): json.dumps(package_json, indent=2),
        os.path.join(src_path, 'server.js'): server_js,
        os.path.join(src_path, 'app.js'): app_js,
        os.path.join(src_path, 'controllers', 'incidentController.js'): incident_controller,
        os.path.join(src_path, 'routes', 'incidentRoutes.js'): incident_routes,
        os.path.join(backend_path, 'data', 'incidents.json'): json.dumps(initial_data, indent=2)
    }

    for path_name, content in file_map.items():
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📝 Written: {os.path.basename(path_name)}")

    print("\n" + "=" * 50)
    print("✅ Backend Setup Complete!")
    print("=" * 50)
    print("NEXT STEPS:")
    print("1. Open a NEW terminal.")
    print("2. cd backend")
    print("3. npm install")
    print("4. npm run dev")


if __name__ == "__main__":
    setup_backend()