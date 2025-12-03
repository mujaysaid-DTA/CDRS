import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Pages
import ReportIncident from './pages/ReportIncident';
import IncidentList from './pages/IncidentList';
import IncidentMap from './pages/IncidentMap';
import Resources from './pages/Resources';
import AdminPanel from './pages/AdminPanel';
import Login from './pages/Login';
import Register from './pages/Register';

function Home() {
  return (
    <div className="App">
      {/* Background Animated Orbs */}
      <div className="bg-orb orb-1"></div>
      <div className="bg-orb orb-2"></div>
      <div className="bg-orb orb-3"></div>

      <header className="App-header">
        <div className="hero-content">
          <h1>Disaster Response<br />System</h1>
          <p className="subtitle">Real-time crowdsourcing for emergency coordination.</p>

          <div className="features-grid">
            <div className="feature-card">
              <span className="icon">📍</span>
              <h3>Report</h3>
              <p>Geolocation-based incident reporting for rapid response.</p>
            </div>

            <div className="feature-card">
              <span className="icon">🗺️</span>
              <h3>Live Map</h3>
              <p>Interactive visualization of active threats in your area.</p>
            </div>

            <div className="feature-card">
              <span className="icon">🤝</span>
              <h3>Volunteer</h3>
              <p>Connect supplies and aid directly to those in need.</p>
            </div>
          </div>

          <div className="cta-buttons">
            <Link to="/report" className="cta-button primary">Report Incident</Link>
            <Link to="/map" className="cta-button secondary">View Map</Link>
            <Link to="/resources" className="cta-button secondary">Volunteer</Link>
            <Link to="/login" className="cta-button secondary">Login</Link>
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
        <Route path="/resources" element={<Resources />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;
