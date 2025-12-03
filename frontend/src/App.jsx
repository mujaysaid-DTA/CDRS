import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import IncidentList from './pages/IncidentList';
import ReportIncident from './pages/ReportIncident';
import AdminPanel from './pages/AdminPanel';
import IncidentMap from './pages/IncidentMap';
import Resources from './pages/Resources';
import Chat from './pages/Chat'; // The new Chat import
import './App.css';

function App() {
  return (
    <div className="App">
      <nav className="navbar">
        <div className="logo">ResQ</div>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/incidents">Incidents</Link>
          <Link to="/report">Report</Link>
          <Link to="/map">Map</Link>
          <Link to="/resources">Resources</Link>
          <Link to="/chat">Chat</Link> {/* Added Chat Link */}
        </div>
      </nav>

      <div className="content">
        <Routes>
          <Route path="/" element={
            <header className="hero">
              <h1>Disaster Response Coordination</h1>
              <p>Real-time reporting and resource management.</p>
              <div className="cta-group">
                <Link to="/login" className="cta-button secondary">Login</Link>
                <Link to="/chat" className="cta-button primary">🔴 Live Chat</Link>
              </div>
            </header>
          } />
          <Route path="/incidents" element={<IncidentList />} />
          <Route path="/report" element={<ReportIncident />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/map" element={<IncidentMap />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/chat" element={<Chat />} /> {/* The new Route */}
        </Routes>
      </div>
    </div>
  );
}

export default App;