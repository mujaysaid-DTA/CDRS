import os


def update_report_page():
    """
    Updates ReportIncident.jsx to connect with the Backend API
    """
    # Path to the file
    file_path = os.path.join(os.getcwd(), 'frontend', 'src', 'pages', 'ReportIncident.jsx')

    print("🔌 Wiring up ReportIncident page to Backend API...\n")

    # The updated React Component
    react_code = '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ReportIncident.css'; // We will assume you have basic CSS or use inline styles for now

function ReportIncident() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    title: '',
    type: 'other',
    severity: 'medium',
    description: '',
    address: '', // We'll map this to location.address
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // 1. Format the data for the Backend
    const payload = {
      title: formData.title,
      type: formData.type,
      severity: formData.severity,
      description: formData.description,
      location: {
        address: formData.address,
        coordinates: [0, 0] // Placeholder until we add the Map picker
      }
    };

    try {
      // 2. Send POST request
      const response = await fetch('http://localhost:5000/api/v1/incidents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to submit report');
      }

      // 3. On success, redirect to the list
      console.log("Report submitted successfully!");
      navigate('/incidents');

    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="report-container" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>📢 Report an Incident</h1>
      <p style={{ color: '#666', marginBottom: '2rem' }}>
        Please provide accurate details to help responders.
      </p>

      {error && (
        <div style={{ padding: '1rem', background: '#fee2e2', color: '#dc2626', borderRadius: '8px', marginBottom: '1rem' }}>
          Error: {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

        {/* Title */}
        <div className="form-group">
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Title</label>
          <input
            type="text"
            name="title"
            required
            value={formData.title}
            onChange={handleChange}
            placeholder="E.g., Flooding on 5th Avenue"
            style={{ width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' }}
          />
        </div>

        {/* Type & Severity Row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Type</label>
            <select
              name="type"
              value={formData.type}
              onChange={handleChange}
              style={{ width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' }}
            >
              <option value="flood">🌊 Flood</option>
              <option value="fire">🔥 Fire</option>
              <option value="accident">🚗 Accident</option>
              <option value="medical">🏥 Medical</option>
              <option value="storm">⛈️ Storm</option>
              <option value="other">⚠️ Other</option>
            </select>
          </div>

          <div className="form-group">
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Severity</label>
            <select
              name="severity"
              value={formData.severity}
              onChange={handleChange}
              style={{ width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' }}
            >
              <option value="low">🟢 Low</option>
              <option value="medium">🟡 Medium</option>
              <option value="high">🟠 High</option>
              <option value="critical">🔴 Critical</option>
            </select>
          </div>
        </div>

        {/* Location */}
        <div className="form-group">
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Location (Address)</label>
          <input
            type="text"
            name="address"
            required
            value={formData.address}
            onChange={handleChange}
            placeholder="E.g., 123 Main St, Lagos"
            style={{ width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' }}
          />
        </div>

        {/* Description */}
        <div className="form-group">
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Description</label>
          <textarea
            name="description"
            rows="4"
            required
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the situation..."
            style={{ width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' }}
          />
        </div>

        {/* Submit Button */}
        <button 
          type="submit" 
          disabled={loading}
          style={{
            padding: '1rem',
            background: loading ? '#9ca3af' : '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: 'background 0.3s'
          }}
        >
          {loading ? 'Submitting Report...' : '📢 Submit Report'}
        </button>
      </form>
    </div>
  );
}

export default ReportIncident;
'''

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(react_code)

    print(f"✅ Updated {os.path.basename(file_path)}")
    print("The form now POSTs data to http://localhost:5000/api/v1/incidents")


if __name__ == "__main__":
    update_report_page()