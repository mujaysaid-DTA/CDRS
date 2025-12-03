const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/incidents.json');

const readData = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE));
};

const writeData = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

exports.getIncidents = (req, res) => {
  const incidents = readData();
  res.json(incidents.reverse()); // Newest first
};

exports.createIncident = (req, res) => {
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
    verified: false, // New Field
    upvotes: 0,
    affectedCount: 1,
    reporter: { name: 'Anonymous', verified: false },
    createdAt: new Date().toISOString(),
    images: []
  };

  incidents.push(newIncident);
  writeData(incidents);
  res.status(201).json(newIncident);
};

// --- NEW ADMIN POWERS ---

exports.verifyIncident = (req, res) => {
  const { id } = req.params;
  const incidents = readData();
  const index = incidents.findIndex(i => i.id === id);

  if (index !== -1) {
    incidents[index].verified = true;
    incidents[index].status = 'verified';
    incidents[index].reporter.verified = true;
    writeData(incidents);
    res.json(incidents[index]);
  } else {
    res.status(404).json({ message: 'Incident not found' });
  }
};

exports.deleteIncident = (req, res) => {
  const { id } = req.params;
  let incidents = readData();
  const initialLength = incidents.length;

  incidents = incidents.filter(i => i.id !== id);

  if (incidents.length < initialLength) {
    writeData(incidents);
    res.json({ message: 'Incident deleted successfully' });
  } else {
    res.status(404).json({ message: 'Incident not found' });
  }
};
