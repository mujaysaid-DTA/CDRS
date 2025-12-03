import os


def setup_admin():
    base_path = os.getcwd()
    backend_src = os.path.join(base_path, 'backend', 'src')
    frontend_src = os.path.join(base_path, 'frontend', 'src')

    print("🛡️  Constructing Admin Control Room...\n")

    # --- PART 1: BACKEND UPGRADE (Power to Delete & Verify) ---

    # 1. Update incidentController.js
    inc_controller_path = os.path.join(backend_src, 'controllers', 'incidentController.js')

    # We are rewriting the whole file to ensure clean structure for the new methods
    inc_controller_code = '''const fs = require('fs');
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
'''

    # 2. Update incidentRoutes.js
    inc_routes_path = os.path.join(backend_src, 'routes', 'incidentRoutes.js')
    inc_routes_code = '''const express = require('express');
const router = express.Router();
const { getIncidents, createIncident, verifyIncident, deleteIncident } = require('../controllers/incidentController');

router.get('/', getIncidents);
router.post('/', createIncident);
router.patch('/:id/verify', verifyIncident); // Admin: Trust
router.delete('/:id', deleteIncident);       // Admin: Ban

module.exports = router;
'''

    with open(inc_controller_path, 'w', encoding='utf-8') as f:
        f.write(inc_controller_code)
    with open(inc_routes_path, 'w', encoding='utf-8') as f:
        f.write(inc_routes_code)
    print("✅ Backend Upgraded (Verify & Delete Routes Added)")

    # --- PART 2: FRONTEND ADMIN PANEL ---

    # 3. AdminPanel.jsx
    admin_page_path = os.path.join(frontend_src, 'pages', 'AdminPanel.jsx')
    admin_page_code = '''import React, { useState, useEffect } from 'react';
import './AdminPanel.css';

function AdminPanel() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [passcode, setPasscode] = useState('');
  const [incidents, setIncidents] = useState([]);
  const [refresh, setRefresh] = useState(0);

  // Simple Gatekeeper
  const handleLogin = (e) => {
    e.preventDefault();
    if (passcode === 'admin123') {
      setIsAuthenticated(true);
    } else {
      alert("Access Denied: Wrong Security Code");
    }
  };

  // Fetch Data
  useEffect(() => {
    if (isAuthenticated) {
      fetch('http://localhost:5000/api/v1/incidents')
        .then(res => res.json())
        .then(data => setIncidents(data))
        .catch(err => console.error(err));
    }
  }, [isAuthenticated, refresh]);

  // Actions
  const verifyIncident = async (id) => {
    if(!window.confirm("Mark this report as Verified/Official?")) return;
    await fetch(`http://localhost:5000/api/v1/incidents/${id}/verify`, { method: 'PATCH' });
    setRefresh(refresh + 1);
  };

  const deleteIncident = async (id) => {
    if(!window.confirm("Are you sure? This cannot be undone.")) return;
    await fetch(`http://localhost:5000/api/v1/incidents/${id}`, { method: 'DELETE' });
    setRefresh(refresh + 1);
  };

  if (!isAuthenticated) {
    return (
      <div className="admin-login">
        <div className="login-box">
          <h2>🛡️ Admin Access</h2>
          <form onSubmit={handleLogin}>
            <input 
              type="password" 
              placeholder="Enter Security Code" 
              value={passcode}
              onChange={e => setPasscode(e.target.value)}
            />
            <button type="submit">Unlock Dashboard</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <header className="admin-header">
        <h1>⚙️ System Administration</h1>
        <button onClick={() => setIsAuthenticated(false)} className="logout-btn">Logout</button>
      </header>

      <div className="admin-content">
        <h3>🚨 Incident Moderation Queue ({incidents.length})</h3>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Status</th>
                <th>Type</th>
                <th>Title</th>
                <th>Location</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map(inc => (
                <tr key={inc.id} className={inc.verified ? 'verified-row' : ''}>
                  <td>
                    {inc.verified ? 
                      <span className="badge verified">✓ Verified</span> : 
                      <span className="badge pending">Pending</span>
                    }
                  </td>
                  <td>{inc.type}</td>
                  <td>{inc.title}</td>
                  <td className="loc-cell">{inc.location.address}</td>
                  <td className="actions-cell">
                    {!inc.verified && (
                      <button className="btn-verify" onClick={() => verifyIncident(inc.id)}>✓ Trust</button>
                    )}
                    <button className="btn-delete" onClick={() => deleteIncident(inc.id)}>🗑️ Ban</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AdminPanel;
'''

    # 4. AdminPanel.css
    admin_css_path = os.path.join(frontend_src, 'pages', 'AdminPanel.css')
    admin_css_code = '''/* Login Screen */
.admin-login {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #1f2937;
}

.login-box {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  width: 400px;
}

.login-box input {
  width: 100%;
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1.1rem;
}

.login-box button {
  width: 100%;
  padding: 1rem;
  background: #111827;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

/* Dashboard */
.admin-panel {
  min-height: 100vh;
  background: #f3f4f6;
}

.admin-header {
  background: #111827;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-btn {
  background: #374151;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.admin-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  overflow: hidden;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th { background: #f9fafb; font-weight: 600; }

.verified-row { background: #f0fdf4; }

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.badge.verified { background: #10b981; color: white; }
.badge.pending { background: #f59e0b; color: white; }

.actions-cell { display: flex; gap: 0.5rem; }

.btn-verify {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete:hover { background: #dc2626; }
'''

    # Write frontend files
    with open(admin_page_path, 'w', encoding='utf-8') as f:
        f.write(admin_page_code)
    with open(admin_css_path, 'w', encoding='utf-8') as f:
        f.write(admin_css_code)

    # 5. Update App.jsx Route
    app_jsx_path = os.path.join(frontend_src, 'App.jsx')
    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "AdminPanel" not in content:
        content = content.replace(
            "import Resources from './pages/Resources';",
            "import Resources from './pages/Resources';\nimport AdminPanel from './pages/AdminPanel';"
        )
        content = content.replace(
            '<Route path="/resources" element={<Resources />} />',
            '<Route path="/resources" element={<Resources />} />\n        <Route path="/admin" element={<AdminPanel />} />'
        )
        # Add a Footer link for Admin (subtle)
        if '<footer' not in content:
            # Inject a footer if it doesn't exist (e.g. at end of Home or just route)
            # Simplest way: just add the route. We can access via URL.
            pass

        with open(app_jsx_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ App.jsx updated with /admin Route")

    print("\n🎉 Admin Dashboard Ready!")


if __name__ == "__main__":
    setup_admin()