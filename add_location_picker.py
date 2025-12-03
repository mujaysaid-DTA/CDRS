import os


def add_location_picker():
    base_path = os.getcwd()
    src_path = os.path.join(base_path, 'frontend', 'src')
    components_map_path = os.path.join(src_path, 'components', 'map')
    pages_path = os.path.join(src_path, 'pages')

    print("📍 Adding Location Picker System...\n")

    # 1. Create LocationPicker.jsx (The Mini Map)
    picker_code = '''import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix Leaflet Icons
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Helper component to handle clicks
function MapEvents({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      onLocationSelect(e.latlng);
    },
  });
  return null;
}

const LocationPicker = ({ onLocationSelect }) => {
  const [position, setPosition] = useState(null);

  const handleSelect = (latlng) => {
    setPosition(latlng);
    onLocationSelect(latlng); // Send back to parent form
  };

  return (
    <div style={{ height: '300px', width: '100%', marginBottom: '1rem', borderRadius: '8px', overflow: 'hidden', border: '2px solid #e5e7eb' }}>
      <MapContainer 
        center={[9.0820, 8.6753]} // Default: Nigeria
        zoom={6} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        <MapEvents onLocationSelect={handleSelect} />
        {position && <Marker position={position} />}
      </MapContainer>
      <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>
        {position ? `Selected: ${position.lat.toFixed(4)}, ${position.lng.toFixed(4)}` : "Tap on the map to pin location"}
      </p>
    </div>
  );
};

export default LocationPicker;
'''

    # 2. Update ReportIncident.jsx (To use the Picker)
    report_page_code = '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LocationPicker from '../components/map/LocationPicker';
import './ReportIncident.css';

function ReportIncident() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [coordinates, setCoordinates] = useState(null); // Store GPS

  const [formData, setFormData] = useState({
    title: '',
    type: 'other',
    severity: 'medium',
    description: '',
    address: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLocationSelect = (latlng) => {
    setCoordinates([latlng.lat, latlng.lng]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validation
    if (!coordinates) {
        setError("Please click on the map to set a location.");
        setLoading(false);
        return;
    }

    const payload = {
      ...formData,
      location: {
        address: formData.address,
        coordinates: coordinates // Now sending Real GPS!
      }
    };

    try {
      const response = await fetch('http://localhost:5000/api/v1/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Failed to submit report');

      navigate('/incidents'); // Go to list

    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="report-container" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>📢 Report an Incident</h1>

      {error && (
        <div style={{ padding: '1rem', background: '#fee2e2', color: '#dc2626', borderRadius: '8px', marginBottom: '1rem' }}>
          Error: {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

        <div className="form-group">
          <label style={{ fontWeight: 'bold' }}>Title</label>
          <input type="text" name="title" required value={formData.title} onChange={handleChange} style={inputStyle} placeholder="E.g. Flood" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label style={{ fontWeight: 'bold' }}>Type</label>
            <select name="type" value={formData.type} onChange={handleChange} style={inputStyle}>
              <option value="flood">🌊 Flood</option>
              <option value="fire">🔥 Fire</option>
              <option value="accident">🚗 Accident</option>
              <option value="medical">🏥 Medical</option>
              <option value="storm">⛈️ Storm</option>
              <option value="other">⚠️ Other</option>
            </select>
          </div>
          <div className="form-group">
            <label style={{ fontWeight: 'bold' }}>Severity</label>
            <select name="severity" value={formData.severity} onChange={handleChange} style={inputStyle}>
              <option value="low">🟢 Low</option>
              <option value="medium">🟡 Medium</option>
              <option value="high">🟠 High</option>
              <option value="critical">🔴 Critical</option>
            </select>
          </div>
        </div>

        {/* The New Location Picker */}
        <div className="form-group">
          <label style={{ fontWeight: 'bold', marginBottom: '0.5rem', display: 'block' }}>Pin Location (Required)</label>
          <LocationPicker onLocationSelect={handleLocationSelect} />
        </div>

        <div className="form-group">
          <label style={{ fontWeight: 'bold' }}>Address Description</label>
          <input type="text" name="address" required value={formData.address} onChange={handleChange} style={inputStyle} placeholder="E.g. Near the Central Bank" />
        </div>

        <div className="form-group">
          <label style={{ fontWeight: 'bold' }}>Description</label>
          <textarea name="description" rows="4" required value={formData.description} onChange={handleChange} style={inputStyle} />
        </div>

        <button type="submit" disabled={loading} style={btnStyle}>
          {loading ? 'Submitting...' : '📢 Submit Report'}
        </button>
      </form>
    </div>
  );
}

const inputStyle = { width: '100%', padding: '0.8rem', borderRadius: '6px', border: '1px solid #ddd' };
const btnStyle = { padding: '1rem', background: '#667eea', color: 'white', border: 'none', borderRadius: '8px', fontSize: '1.1rem', cursor: 'pointer' };

export default ReportIncident;
'''

    # Write files
    with open(os.path.join(components_map_path, 'LocationPicker.jsx'), 'w', encoding='utf-8') as f:
        f.write(picker_code)

    with open(os.path.join(pages_path, 'ReportIncident.jsx'), 'w', encoding='utf-8') as f:
        f.write(report_page_code)

    print("✅ Location Picker Integrated!")


if __name__ == "__main__":
    add_location_picker()