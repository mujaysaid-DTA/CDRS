const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/resources.json');

const readData = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE));
};

const writeData = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

exports.getResources = (req, res) => {
  const resources = readData();
  // Return newest first
  res.json(resources.reverse());
};

exports.createResource = (req, res) => {
  const { type, item, quantity, location, contact } = req.body;
  const resources = readData();

  const newResource = {
    id: uuidv4(),
    category: 'request', // Always a request now
    type,
    item,
    quantity,
    location,
    contact,
    status: 'pending', // pending | fulfilled
    createdAt: new Date().toISOString()
  };

  resources.push(newResource); // Add to end (we reverse on get)
  writeData(resources);
  res.status(201).json(newResource);
};

exports.updateResourceStatus = (req, res) => {
  const { id } = req.params;
  const { status } = req.body; // Expecting 'fulfilled'

  let resources = readData();
  const index = resources.findIndex(r => r.id === id);

  if (index !== -1) {
    resources[index].status = status;
    writeData(resources);
    res.json(resources[index]);
  } else {
    res.status(404).json({ message: 'Resource not found' });
  }
};
