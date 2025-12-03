import API_BASE_URL from '../config';
import React, { useState, useEffect } from 'react';
import MapView from '../components/map/MapView';
import './IncidentMap.css';

function IncidentMap() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch real data from backend
    fetch(`${API_BASE_URL}/incidents')
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
