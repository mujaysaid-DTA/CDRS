import os


def upgrade_volunteer_hub():
    base_path = os.getcwd()
    backend_src = os.path.join(base_path, 'backend', 'src')
    frontend_src = os.path.join(base_path, 'frontend', 'src')

    print("🚀 Upgrading to Volunteer Hub...\n")

    # --- PART 1: BACKEND UPGRADE (Enable Status Updates) ---

    # 1. Update resourceController.js to handle status changes
    controller_path = os.path.join(backend_src, 'controllers', 'resourceController.js')
    controller_code = '''const fs = require('fs');
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
'''

    # 2. Update resourceRoutes.js to add the PATCH endpoint
    routes_path = os.path.join(backend_src, 'routes', 'resourceRoutes.js')
    routes_code = '''const express = require('express');
const router = express.Router();
const { getResources, createResource, updateResourceStatus } = require('../controllers/resourceController');

router.get('/', getResources);
router.post('/', createResource);
router.patch('/:id', updateResourceStatus); // New route for updates

module.exports = router;
'''

    with open(controller_path, 'w', encoding='utf-8') as f:
        f.write(controller_code)
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(routes_code)
    print("✅ Backend Logic Updated (Added Status Switching)")

    # --- PART 2: FRONTEND UPGRADE (New UI) ---

    # 3. Resources.jsx
    resources_jsx_path = os.path.join(frontend_src, 'pages', 'Resources.jsx')
    resources_jsx = '''import React, { useState, useEffect } from 'react';
import './Resources.css';

function Resources() {
  const [activeTab, setActiveTab] = useState('request'); // 'request' or 'volunteer'
  const [resources, setResources] = useState([]);
  const [formData, setFormData] = useState({
    type: 'food', item: '', quantity: '', location: '', contact: ''
  });

  // Fetch Data
  const fetchResources = () => {
    fetch('http://localhost:5000/api/v1/resources')
      .then(res => res.json())
      .then(data => setResources(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchResources();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('http://localhost:5000/api/v1/resources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    fetchResources();
    setFormData({ type: 'food', item: '', quantity: '', location: '', contact: '' });
    alert("Request Broadcasted!");
  };

  const handleMarkFulfilled = async (id) => {
    await fetch(`http://localhost:5000/api/v1/resources/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'fulfilled' })
    });
    fetchResources();
  };

  const isVolunteer = activeTab === 'volunteer';

  return (
    <div className="resources-page">
      <header className="res-header">
        <h1>🤝 Community Aid</h1>
        <div className="tabs">
          <button 
            className={`tab ${!isVolunteer ? 'active req' : ''}`}
            onClick={() => setActiveTab('request')}
          >
            🆘 Request Aid
          </button>
          <button 
            className={`tab ${isVolunteer ? 'active vol' : ''}`}
            onClick={() => setActiveTab('volunteer')}
          >
            🙌 Volunteer Hub
          </button>
        </div>
      </header>

      <div className="res-content">

        {/* VIEW 1: REQUEST AID (Form Only) */}
        {!isVolunteer && (
          <div className="request-section">
            <form className="res-form" onSubmit={handleSubmit}>
              <h3>📢 Broadcast a Need</h3>
              <p className="form-hint">Your request will be visible to all volunteers immediately.</p>

              <div className="form-group">
                  <label>Category</label>
                  <select onChange={e => setFormData({...formData, type: e.target.value})} value={formData.type}>
                    <option value="food">🍱 Food</option>
                    <option value="water">💧 Water</option>
                    <option value="medical">💊 Medical</option>
                    <option value="shelter">⛺ Shelter</option>
                    <option value="transport">🚚 Transport</option>
                  </select>
              </div>

              <input 
                  placeholder="What is needed? (e.g. 20 Blankets)" 
                  value={formData.item}
                  onChange={e => setFormData({...formData, item: e.target.value})} 
                  required 
              />

              <div className="row-inputs">
                  <input 
                      placeholder="Quantity" 
                      value={formData.quantity}
                      onChange={e => setFormData({...formData, quantity: e.target.value})} 
                      required 
                  />
                  <input 
                      placeholder="Contact Number" 
                      value={formData.contact}
                      onChange={e => setFormData({...formData, contact: e.target.value})} 
                      required 
                  />
              </div>

              <input 
                  placeholder="Location / Address" 
                  value={formData.location}
                  onChange={e => setFormData({...formData, location: e.target.value})} 
                  required 
              />

              <button type="submit" className="submit-req">Broadcast Request</button>
            </form>
          </div>
        )}

        {/* VIEW 2: VOLUNTEER HUB (List Only) */}
        {isVolunteer && (
          <div className="volunteer-section">
            <div className="hub-header">
                <h2>📋 Active Needs Queue</h2>
                <p>Select a task to help your community.</p>
            </div>

            <div className="res-grid">
              {resources.map(res => (
                <div key={res.id} className={`res-card ${res.status === 'fulfilled' ? 'fulfilled' : ''}`}>

                  {/* The Ticker / Mark */}
                  {res.status === 'fulfilled' && (
                      <div className="status-badge">✅ ANSWERED</div>
                  )}

                  <div className="card-top">
                    <span className="icon">
                        {res.type === 'food' ? '🍱' : 
                         res.type === 'water' ? '💧' : 
                         res.type === 'medical' ? '💊' : '🆘'}
                    </span>
                    <span className="time">{new Date(res.createdAt).toLocaleDateString()}</span>
                  </div>

                  <h3 style={{ textDecoration: res.status === 'fulfilled' ? 'line-through' : 'none' }}>
                    {res.item}
                  </h3>

                  <div className="card-details">
                    <p><strong>Qty:</strong> {res.quantity}</p>
                    <p><strong>📍</strong> {res.location}</p>
                    <p><strong>📞</strong> {res.contact}</p>
                  </div>

                  {res.status !== 'fulfilled' ? (
                    <button className="volunteer-btn" onClick={() => handleMarkFulfilled(res.id)}>
                        🙌 I can handle this
                    </button>
                  ) : (
                    <button className="volunteer-btn disabled" disabled>
                        Help on the way
                    </button>
                  )}
                </div>
              ))}
            </div>

            {resources.length === 0 && <p className="empty">No active requests. Good news!</p>}
          </div>
        )}

        {/* Optional: Show My Requests underneath the form for context */}
        {!isVolunteer && resources.length > 0 && (
            <div className="my-requests-preview">
                <h4>Recent Community Requests</h4>
                <div className="mini-list">
                    {resources.slice(0,3).map(r => (
                        <div key={r.id} className="mini-item">
                            <span>{r.item}</span>
                            <span className={`status-dot ${r.status}`}>
                                {r.status === 'fulfilled' ? '✅ Answered' : '⏳ Pending'}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        )}
      </div>
    </div>
  );
}

export default Resources;
'''

    # 4. Resources.css
    resources_css_path = os.path.join(frontend_src, 'pages', 'Resources.css')
    resources_css = '''.resources-page {
  padding: 2rem;
  max-width: 1000px;
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
  border-radius: 30px;
  transition: all 0.3s;
  color: #555;
}

.tab.active.req { background: #ef4444; color: white; transform: scale(1.05); }
.tab.active.vol { background: #3b82f6; color: white; transform: scale(1.05); }

/* Form Styles */
.res-form {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15);
  border: 2px solid #fee2e2;
}

.res-form h3 { color: #ef4444; margin-bottom: 0.5rem; }
.form-hint { color: #888; margin-bottom: 1.5rem; font-size: 0.9rem; }

.res-form input, .res-form select {
  width: 100%;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.row-inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.submit-req {
  width: 100%;
  padding: 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}
.submit-req:hover { background: #dc2626; }

/* Volunteer Hub Styles */
.hub-header { text-align: center; margin-bottom: 2rem; color: #3b82f6; }

.res-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.res-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  position: relative;
  overflow: hidden;
  border-top: 4px solid #3b82f6;
  transition: transform 0.2s;
}

.res-card:hover { transform: translateY(-5px); }

.res-card.fulfilled {
  background: #f3f4f6;
  border-top-color: #10b981;
  opacity: 0.8;
}

.status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #10b981;
  color: white;
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 10px;
  font-weight: bold;
}

.card-top { display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; }
.icon { font-size: 1.5rem; }
.time { font-size: 0.8rem; color: #999; }

.card-details {
  background: #f9fafb;
  padding: 0.8rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.volunteer-btn {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  background: #3b82f6;
  color: white;
  transition: 0.3s;
}

.volunteer-btn:hover { background: #2563eb; }

.volunteer-btn.disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: default;
}

/* Mini List for Requester */
.my-requests-preview { margin-top: 3rem; }
.mini-list { background: white; padding: 1rem; border-radius: 10px; }
.mini-item { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee; }
.status-dot.fulfilled { color: #10b981; font-weight: bold; }
.status-dot.pending { color: #f59e0b; }
'''

    with open(resources_jsx_path, 'w', encoding='utf-8') as f:
        f.write(resources_jsx)
    with open(resources_css_path, 'w', encoding='utf-8') as f:
        f.write(resources_css)

    print("✅ Frontend Transformed (Volunteer Hub + Ticker)")
    print("\nIMPORTANT: Restart your Backend Server to apply the new logic!")


if __name__ == "__main__":
    upgrade_volunteer_hub()
