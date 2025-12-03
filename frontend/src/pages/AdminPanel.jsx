import API_BASE_URL from '../config';
import React, { useState, useEffect } from 'react';
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
      fetch(`${API_BASE_URL}/incidents')
        .then(res => res.json())
        .then(data => setIncidents(data))
        .catch(err => console.error(err));
    }
  }, [isAuthenticated, refresh]);

  // Actions
  const verifyIncident = async (id) => {
    if(!window.confirm("Mark this report as Verified/Official?")) return;
    await fetch(`${API_BASE_URL}/incidents/${id}/verify`, { method: 'PATCH' });
    setRefresh(refresh + 1);
  };

  const deleteIncident = async (id) => {
    if(!window.confirm("Are you sure? This cannot be undone.")) return;
    await fetch(`${API_BASE_URL}/incidents/${id}`, { method: 'DELETE' });
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
