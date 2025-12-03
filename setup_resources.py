import os
import json


def setup_resources():
    base_path = os.getcwd()

    # Paths
    backend_src = os.path.join(base_path, 'backend', 'src')
    frontend_src = os.path.join(base_path, 'frontend', 'src')
    data_path = os.path.join(base_path, 'backend', 'data', 'resources.json')

    print("🤝 Building Resource Management System...\n")

    # --- PART 1: BACKEND ---

    # 1. Create Data File
    if not os.path.exists(data_path):
        with open(data_path, 'w') as f:
            f.write('[]')

    # 2. resourceController.js
    res_controller = '''const fs = require('fs');
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
  res.json(resources);
};

exports.createResource = (req, res) => {
  const { category, type, item, quantity, location, contact } = req.body;
  const resources = readData();

  const newResource = {
    id: uuidv4(),
    category, // 'request' or 'offer'
    type,     // 'food', 'water', 'medical', 'shelter'
    item,
    quantity,
    location,
    contact,
    status: 'active',
    createdAt: new Date().toISOString()
  };

  resources.unshift(newResource);
  writeData(resources);
  res.status(201).json(newResource);
};
'''

    # 3. resourceRoutes.js
    res_routes = '''const express = require('express');
const router = express.Router();
const { getResources, createResource } = require('../controllers/resourceController');

router.get('/', getResources);
router.post('/', createResource);

module.exports = router;
'''

    # 4. Update app.js to include the new route
    # We read the existing file and inject the new route
    app_js_path = os.path.join(backend_src, 'app.js')
    with open(app_js_path, 'r', encoding='utf-8') as f:
        app_content = f.read()

    if "resourceRoutes" not in app_content:
        # Inject require
        app_content = app_content.replace(
            "const incidentRoutes = require('./routes/incidentRoutes');",
            "const incidentRoutes = require('./routes/incidentRoutes');\nconst resourceRoutes = require('./routes/resourceRoutes');"
        )
        # Inject use
        app_content = app_content.replace(
            "app.use('/api/v1/incidents', incidentRoutes);",
            "app.use('/api/v1/incidents', incidentRoutes);\napp.use('/api/v1/resources', resourceRoutes);"
        )
        with open(app_js_path, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print("✅ Updated app.js with Resource Routes")

    # Write Backend Files
    with open(os.path.join(backend_src, 'controllers', 'resourceController.js'), 'w') as f:
        f.write(res_controller)
    with open(os.path.join(backend_src, 'routes', 'resourceRoutes.js'), 'w') as f:
        f.write(res_routes)

    # --- PART 2: FRONTEND ---

    # 5. Resources.jsx (The Page)
    resources_page = '''import React, { useState, useEffect } from 'react';
import './Resources.css';

function Resources() {
  const [activeTab, setActiveTab] = useState('request'); // 'request' or 'offer'
  const [resources, setResources] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    type: 'food', item: '', quantity: '', location: '', contact: ''
  });

  // Fetch Data
  useEffect(() => {
    fetch('http://localhost:5000/api/v1/resources')
      .then(res => res.json())
      .then(data => setResources(data))
      .catch(err => console.error(err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ...formData, category: activeTab };

    await fetch('http://localhost:5000/api/v1/resources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    // Refresh list
    const res = await fetch('http://localhost:5000/api/v1/resources');
    const data = await res.json();
    setResources(data);
    setShowForm(false);
    setFormData({ type: 'food', item: '', quantity: '', location: '', contact: '' });
  };

  const filteredResources = resources.filter(r => r.category === activeTab);

  return (
    <div className="resources-page">
      <header className="res-header">
        <h1>🤝 Resource Coordination</h1>
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'request' ? 'active req' : ''}`}
            onClick={() => setActiveTab('request')}
          >
            I Need Help 🆘
          </button>
          <button 
            className={`tab ${activeTab === 'offer' ? 'active off' : ''}`}
            onClick={() => setActiveTab('offer')}
          >
            I Can Help 📦
          </button>
        </div>
      </header>

      <div className="res-content">
        <button className="add-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : `+ New ${activeTab === 'request' ? 'Request' : 'Offer'}`}
        </button>

        {showForm && (
          <form className="res-form" onSubmit={handleSubmit}>
            <select onChange={e => setFormData({...formData, type: e.target.value})}>
              <option value="food">🍱 Food</option>
              <option value="water">💧 Water</option>
              <option value="medical">💊 Medical</option>
              <option value="shelter">⛺ Shelter</option>
            </select>
            <input placeholder="Item Name (e.g. Rice bags)" onChange={e => setFormData({...formData, item: e.target.value})} required />
            <input placeholder="Quantity" onChange={e => setFormData({...formData, quantity: e.target.value})} required />
            <input placeholder="Location" onChange={e => setFormData({...formData, location: e.target.value})} required />
            <input placeholder="Contact Info" onChange={e => setFormData({...formData, contact: e.target.value})} required />
            <button type="submit">Submit</button>
          </form>
        )}

        <div className="res-grid">
          {filteredResources.map(res => (
            <div key={res.id} className={`res-card ${res.category}`}>
              <div className="card-top">
                <span className="icon">{res.type === 'food' ? '🍱' : res.type === 'water' ? '💧' : res.type === 'medical' ? '💊' : '⛺'}</span>
                <span className="time">{new Date(res.createdAt).toLocaleTimeString()}</span>
              </div>
              <h3>{res.item}</h3>
              <p className="qty">Quantity: {res.quantity}</p>
              <p className="loc">📍 {res.location}</p>
              <p className="contact">📞 {res.contact}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Resources;
'''

    # 6. Resources.css
    resources_css = '''.resources-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.res-header { text-align: center; margin-bottom: 2rem; }

.tabs { display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; }

.tab {
  padding: 1rem 2rem;
  border: none;
  background: #e5e7eb;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  border-radius: 8px;
  opacity: 0.7;
  transition: all 0.3s;
}

.tab.active { opacity: 1; transform: scale(1.05); color: white; }
.tab.active.req { background: #ef4444; }
.tab.active.off { background: #10b981; }

.add-btn {
  display: block;
  width: 100%;
  padding: 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  margin-bottom: 2rem;
}

.res-form {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.res-form input, .res-form select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.res-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.res-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  border-left: 5px solid #ccc;
}

.res-card.request { border-left-color: #ef4444; }
.res-card.offer { border-left-color: #10b981; }

.card-top { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
.icon { font-size: 1.5rem; }
.time { font-size: 0.8rem; color: #888; }
.qty, .loc, .contact { margin: 0.3rem 0; color: #555; font-size: 0.95rem; }
'''

    with open(os.path.join(frontend_src, 'pages', 'Resources.jsx'), 'w', encoding='utf-8') as f:
        f.write(resources_page)
    with open(os.path.join(frontend_src, 'pages', 'Resources.css'), 'w', encoding='utf-8') as f:
        f.write(resources_css)

    # 7. Add Route to App.jsx
    app_jsx_path = os.path.join(frontend_src, 'App.jsx')
    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "Resources" not in content:
        content = content.replace(
            "import IncidentMap from './pages/IncidentMap';",
            "import IncidentMap from './pages/IncidentMap';\nimport Resources from './pages/Resources';"
        )
        content = content.replace(
            '<Route path="/map" element={<IncidentMap />} />',
            '<Route path="/map" element={<IncidentMap />} />\n        <Route path="/resources" element={<Resources />} />'
        )
        # Add link to Home menu
        content = content.replace(
            '<Link to="/map" className="cta-button secondary" style={{background: \'#10b981\', borderColor: \'#10b981\'}}>View Map</Link>',
            '<Link to="/map" className="cta-button secondary" style={{background: \'#10b981\', borderColor: \'#10b981\'}}>View Map</Link>\n            <Link to="/resources" className="cta-button secondary" style={{background: \'#f59e0b\', borderColor: \'#f59e0b\'}}>Resources</Link>'
        )
        with open(app_jsx_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print("✅ Updated App.jsx with Resources Route")

    print("\n✅ Resource Management System Created!")


if __name__ == "__main__":
    setup_resources()