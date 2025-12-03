import os


def setup_maps():
    base_path = os.getcwd()
    src_path = os.path.join(base_path, 'frontend', 'src')
    components_map_path = os.path.join(src_path, 'components', 'map')
    pages_path = os.path.join(src_path, 'pages')

    print("🗺️  Initializing Map System...\n")

    # Ensure directories exist
    if not os.path.exists(components_map_path):
        os.makedirs(components_map_path)

    # 1. Component: IncidentMarker.jsx (The Pin on the map)
    marker_code = '''import React from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default Leaflet icon issues in React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const IncidentMarker = ({ incident }) => {
  // Color code based on severity
  const getColor = (s) => {
    switch(s) {
      case 'critical': return '#dc2626'; // Red
      case 'high': return '#ea580c';     // Orange
      case 'medium': return '#ca8a04';   // Yellow
      default: return '#2563eb';         // Blue
    }
  };

  // If no coordinates, don't render
  if (!incident.location || !incident.location.coordinates) return null;

  const [lat, lng] = incident.location.coordinates;

  return (
    <Marker position={[lat, lng]}>
      <Popup>
        <div style={{ minWidth: '200px' }}>
          <h3 style={{ margin: '0 0 5px 0', color: getColor(incident.severity) }}>
            {incident.type.toUpperCase()}
          </h3>
          <strong>{incident.title}</strong>
          <p>{incident.description.substring(0, 50)}...</p>
          <small>Severity: {incident.severity}</small>
        </div>
      </Popup>
    </Marker>
  );
};

export default IncidentMarker;
'''

    # 2. Component: MapView.jsx (The Map Container)
    map_view_code = '''import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import IncidentMarker from './IncidentMarker';

// Default center (e.g., Nigeria)
const DEFAULT_CENTER = [9.0820, 8.6753];
const DEFAULT_ZOOM = 6;

const MapView = ({ incidents }) => {
  return (
    <MapContainer 
      center={DEFAULT_CENTER} 
      zoom={DEFAULT_ZOOM} 
      style={{ height: '100%', width: '100%', borderRadius: '15px' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {incidents.map(incident => (
        <IncidentMarker key={incident.id} incident={incident} />
      ))}
    </MapContainer>
  );
};

export default MapView;
'''

    # 3. Page: IncidentMap.jsx (The Full Page View)
    incident_map_page = '''import React, { useState, useEffect } from 'react';
import MapView from '../components/map/MapView';
import './IncidentMap.css';

function IncidentMap() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch real data from backend
    fetch('http://localhost:5000/api/v1/incidents')
      .then(res => res.json())
      .then(data => {
        setIncidents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load map data", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="map-page">
      <div className="map-sidebar">
        <h2>🗺️ Live Incident Map</h2>
        <div className="stats-box">
          <div className="stat">
            <span className="num">{incidents.length}</span>
            <span className="label">Active Incidents</span>
          </div>
          <div className="stat">
            <span className="num" style={{color: '#dc2626'}}>
              {incidents.filter(i => i.severity === 'critical').length}
            </span>
            <span className="label">Critical</span>
          </div>
        </div>
        <p className="instruction">Click on markers to see details.</p>
        <a href="/" className="back-link">← Back Home</a>
      </div>

      <div className="map-wrapper">
        {loading ? <div className="loading">Loading Map Data...</div> : <MapView incidents={incidents} />}
      </div>
    </div>
  );
}

export default IncidentMap;
'''

    # 4. CSS for the Map Page
    map_css = '''.map-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.map-sidebar {
  width: 300px;
  background: white;
  padding: 2rem;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.map-wrapper {
  flex: 1;
  background: #e5e7eb;
  padding: 1rem;
}

.stats-box {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
  padding: 1rem;
  background: #f3f4f6;
  border-radius: 10px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat .num {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2563eb;
}

.stat .label {
  font-size: 0.8rem;
  color: #6b7280;
}

.back-link {
  margin-top: auto;
  text-decoration: none;
  color: #4b5563;
  font-weight: 500;
}

.back-link:hover {
  color: #000;
}
'''

    # Write the files
    files = {
        os.path.join(components_map_path, 'IncidentMarker.jsx'): marker_code,
        os.path.join(components_map_path, 'MapView.jsx'): map_view_code,
        os.path.join(pages_path, 'IncidentMap.jsx'): incident_map_page,
        os.path.join(pages_path, 'IncidentMap.css'): map_css
    }

    for path, content in files.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {os.path.basename(path)}")

    # 5. Update App.jsx to include the new route
    print("\n⚠️  NOTE: I am updating App.jsx to add the /map route...")

    app_jsx_path = os.path.join(src_path, 'App.jsx')
    new_app_jsx = '''import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import ReportIncident from './pages/ReportIncident';
import IncidentList from './pages/IncidentList';
import IncidentMap from './pages/IncidentMap';

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="hero-section">
          <h1>🚨 Disaster Response System</h1>
          <p className="subtitle">Crowdsourcing Emergency Response & Resource Coordination</p>

          <div className="features-grid">
            <div className="feature-card">
              <div className="icon">📍</div>
              <h3>Report Incidents</h3>
              <p>Real-time disaster reporting with geolocation</p>
            </div>

            <div className="feature-card">
              <div className="icon">🗺️</div>
              <h3>Interactive Map</h3>
              <p>View incidents and resources on live map</p>
            </div>

            <div className="feature-card">
              <div className="icon">🤝</div>
              <h3>Resource Matching</h3>
              <p>Connect those in need with available help</p>
            </div>
          </div>

          <div className="cta-buttons">
            <Link to="/report" className="cta-button primary">Report Now</Link>
            <Link to="/incidents" className="cta-button secondary">Browse List</Link>
            <Link to="/map" className="cta-button secondary" style={{background: '#10b981', borderColor: '#10b981'}}>View Map</Link>
          </div>
        </div>
      </header>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/report" element={<ReportIncident />} />
        <Route path="/incidents" element={<IncidentList />} />
        <Route path="/map" element={<IncidentMap />} />
      </Routes>
    </Router>
  );
}

export default App;
'''
    with open(app_jsx_path, 'w', encoding='utf-8') as f:
        f.write(new_app_jsx)
    print("✅ Updated App.jsx with Map Route")


if __name__ == "__main__":
    setup_maps()