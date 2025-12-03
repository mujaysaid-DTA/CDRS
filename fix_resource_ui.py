import os


def fix_resource_ui():
    base_path = os.getcwd()
    file_path = os.path.join(base_path, 'frontend', 'src', 'pages', 'Resources.jsx')

    print("🎨 Polishing Resource UI text...\n")

    updated_code = '''import React, { useState, useEffect } from 'react';
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

  // --- DYNAMIC TEXT HELPERS ---
  const isRequest = activeTab === 'request';

  const formTitle = isRequest ? "🆘 Submit a Help Request" : "📦 Offer Resources";
  const itemPlaceholder = isRequest ? "What do you need? (e.g. Rice, Bandages)" : "What are you offering? (e.g. Generators)";
  const locationPlaceholder = isRequest ? "Where is help needed? (Address/Landmark)" : "Where can this be picked up?";
  const contactPlaceholder = isRequest ? "How can we reach you?" : "Donor Contact Info";
  const submitBtnText = isRequest ? "Broadcase Request" : "Post Offer";

  return (
    <div className="resources-page">
      <header className="res-header">
        <h1>🤝 Resource Coordination</h1>
        <p className="subtitle">Connect needs with available supplies in real-time</p>

        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'request' ? 'active req' : ''}`}
            onClick={() => { setActiveTab('request'); setShowForm(false); }}
          >
            I Need Help 🆘
          </button>
          <button 
            className={`tab ${activeTab === 'offer' ? 'active off' : ''}`}
            onClick={() => { setActiveTab('offer'); setShowForm(false); }}
          >
            I Can Help 📦
          </button>
        </div>
      </header>

      <div className="res-content">
        <button 
            className="add-btn" 
            onClick={() => setShowForm(!showForm)}
            style={{ backgroundColor: isRequest ? '#ef4444' : '#10b981' }}
        >
          {showForm ? 'Cancel' : `+ ${isRequest ? 'Request Aid' : 'Offer Supply'}`}
        </button>

        {showForm && (
          <form className="res-form" onSubmit={handleSubmit} style={{ borderTop: `5px solid ${isRequest ? '#ef4444' : '#10b981'}` }}>
            <h3>{formTitle}</h3>

            <div className="form-group">
                <label>Resource Type</label>
                <select onChange={e => setFormData({...formData, type: e.target.value})} value={formData.type}>
                <option value="food">🍱 Food</option>
                <option value="water">💧 Water</option>
                <option value="medical">💊 Medical</option>
                <option value="shelter">⛺ Shelter</option>
                <option value="transport">🚚 Transport</option>
                </select>
            </div>

            <input 
                placeholder={itemPlaceholder} 
                value={formData.item}
                onChange={e => setFormData({...formData, item: e.target.value})} 
                required 
            />

            <div className="row-inputs">
                <input 
                    placeholder="Quantity (e.g. 50 packs)" 
                    value={formData.quantity}
                    onChange={e => setFormData({...formData, quantity: e.target.value})} 
                    required 
                />
                <input 
                    placeholder={contactPlaceholder} 
                    value={formData.contact}
                    onChange={e => setFormData({...formData, contact: e.target.value})} 
                    required 
                />
            </div>

            <input 
                placeholder={locationPlaceholder} 
                value={formData.location}
                onChange={e => setFormData({...formData, location: e.target.value})} 
                required 
            />

            <button type="submit" style={{ backgroundColor: isRequest ? '#ef4444' : '#10b981' }}>
                {submitBtnText}
            </button>
          </form>
        )}

        {filteredResources.length === 0 ? (
            <div className="empty-state">
                <p>No {activeTab}s found. Be the first to post!</p>
            </div>
        ) : (
            <div className="res-grid">
            {filteredResources.map(res => (
                <div key={res.id} className={`res-card ${res.category}`}>
                <div className="card-top">
                    <span className="icon">
                        {res.type === 'food' ? '🍱' : 
                         res.type === 'water' ? '💧' : 
                         res.type === 'medical' ? '💊' : 
                         res.type === 'shelter' ? '⛺' : '🚚'}
                    </span>
                    <span className="time">{new Date(res.createdAt).toLocaleDateString()}</span>
                </div>
                <h3>{res.item}</h3>
                <div className="card-details">
                    <p><strong>Qty:</strong> {res.quantity}</p>
                    <p><strong>📍</strong> {res.location}</p>
                    <p><strong>📞</strong> {res.contact}</p>
                </div>
                <button className="contact-btn">
                    {res.category === 'request' ? 'Offer Help' : 'Request This'}
                </button>
                </div>
            ))}
            </div>
        )}
      </div>
    </div>
  );
}

export default Resources;
'''

    # We also need to add a bit of CSS to support the new layout
    css_path = os.path.join(base_path, 'frontend', 'src', 'pages', 'Resources.css')
    css_append = '''
.row-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.card-details {
    background: #f9fafb;
    padding: 0.5rem;
    border-radius: 6px;
    margin: 0.5rem 0;
    font-size: 0.9rem;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #888;
    font-size: 1.2rem;
}

.contact-btn {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.5rem;
    border: 1px solid #ddd;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
}

.contact-btn:hover {
    background: #f3f4f6;
    border-color: #bbb;
}
'''

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_code)

    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(css_append)

    print("✅ Resource UI Updated successfully!")


if __name__ == "__main__":
    fix_resource_ui()