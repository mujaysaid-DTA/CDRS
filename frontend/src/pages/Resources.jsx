import API_BASE_URL from '../config';
import React, { useState, useEffect } from 'react';
import './Resources.css';

function Resources() {
  const [activeTab, setActiveTab] = useState('request'); // 'request' or 'volunteer'
  const [resources, setResources] = useState([]);
  const [formData, setFormData] = useState({
    type: 'food', item: '', quantity: '', location: '', contact: ''
  });

  // Fetch Data
  const fetchResources = () => {
    fetch(`${API_BASE_URL}/resources`)
      .then(res => res.json())
      .then(data => setResources(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchResources();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch(`${API_BASE_URL}/resources`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    fetchResources();
    setFormData({ type: 'food', item: '', quantity: '', location: '', contact: '' });
    alert("Request Broadcasted!");
  };

  const handleMarkFulfilled = async (id) => {
    await fetch(`${API_BASE_URL}/resources/${id}`, {
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
