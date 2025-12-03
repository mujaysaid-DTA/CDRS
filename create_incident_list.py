import os


def create_incident_list_files():
    """
    Creates the incident list/browse feature
    """

    frontend_path = os.path.join(os.getcwd(), 'frontend', 'src')

    print("Creating Incident List Feature...\n")

    # pages/IncidentList.jsx
    incident_list_page = '''import React, { useState, useEffect } from 'react';
import './IncidentList.css';

function IncidentList() {
  const [incidents, setIncidents] = useState([]);
  const [filteredIncidents, setFilteredIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [filters, setFilters] = useState({
    type: 'all',
    severity: 'all',
    status: 'all',
    search: ''
  });

  // Mock data - Replace with API call later
  const mockIncidents = [
    {
      id: 1,
      type: 'flood',
      severity: 'critical',
      title: 'Major flooding on Main Street',
      description: 'Water levels rising rapidly. Multiple buildings affected. Immediate evacuation needed.',
      location: { address: 'Main Street, Downtown', coordinates: [9.0765, 7.3986] },
      reporter: { name: 'John Doe', verified: true },
      status: 'verified',
      affectedCount: 50,
      upvotes: 23,
      createdAt: '2 hours ago',
      images: ['flood1.jpg', 'flood2.jpg']
    },
    {
      id: 2,
      type: 'fire',
      severity: 'high',
      title: 'Building fire at Industrial Complex',
      description: 'Large fire reported at warehouse. Fire department on site. Smoke visible from distance.',
      location: { address: 'Industrial Zone, Area 3', coordinates: [9.0820, 7.4010] },
      reporter: { name: 'Sarah Smith', verified: true },
      status: 'in-progress',
      affectedCount: 15,
      upvotes: 18,
      createdAt: '45 minutes ago',
      images: ['fire1.jpg']
    },
    {
      id: 3,
      type: 'accident',
      severity: 'medium',
      title: 'Multi-vehicle accident on Highway 5',
      description: 'Three car collision. Traffic blocked. Ambulance requested. Minor injuries reported.',
      location: { address: 'Highway 5, Exit 12', coordinates: [9.0890, 7.4100] },
      reporter: { name: 'Mike Johnson', verified: false },
      status: 'pending',
      affectedCount: 7,
      upvotes: 5,
      createdAt: '1 hour ago',
      images: []
    },
    {
      id: 4,
      type: 'medical',
      severity: 'high',
      title: 'Medical emergency at Community Center',
      description: 'Person collapsed. CPR being administered. Ambulance on the way.',
      location: { address: 'Community Center, Park Avenue', coordinates: [9.0750, 7.3950] },
      reporter: { name: 'Emily Davis', verified: true },
      status: 'in-progress',
      affectedCount: 1,
      upvotes: 12,
      createdAt: '30 minutes ago',
      images: []
    },
    {
      id: 5,
      type: 'storm',
      severity: 'medium',
      title: 'Severe thunderstorm approaching',
      description: 'Dark clouds forming. Strong winds. Heavy rain expected. Residents advised to stay indoors.',
      location: { address: 'Northern District', coordinates: [9.0950, 7.4200] },
      reporter: { name: 'Weather Watch', verified: true },
      status: 'verified',
      affectedCount: 200,
      upvotes: 45,
      createdAt: '15 minutes ago',
      images: ['storm1.jpg']
    },
    {
      id: 6,
      type: 'other',
      severity: 'low',
      title: 'Power outage in residential area',
      description: 'Electricity cut off since morning. Utility company notified. Expected restoration in 3 hours.',
      location: { address: 'Sunset Boulevard, Block 7', coordinates: [9.0700, 7.3900] },
      reporter: { name: 'Robert Lee', verified: false },
      status: 'resolved',
      affectedCount: 30,
      upvotes: 8,
      createdAt: '4 hours ago',
      images: []
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setIncidents(mockIncidents);
      setFilteredIncidents(mockIncidents);
      setLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = incidents;

    if (filters.type !== 'all') {
      filtered = filtered.filter(inc => inc.type === filters.type);
    }

    if (filters.severity !== 'all') {
      filtered = filtered.filter(inc => inc.severity === filters.severity);
    }

    if (filters.status !== 'all') {
      filtered = filtered.filter(inc => inc.status === filters.status);
    }

    if (filters.search) {
      filtered = filtered.filter(inc =>
        inc.title.toLowerCase().includes(filters.search.toLowerCase()) ||
        inc.description.toLowerCase().includes(filters.search.toLowerCase()) ||
        inc.location.address.toLowerCase().includes(filters.search.toLowerCase())
      );
    }

    setFilteredIncidents(filtered);
  }, [filters, incidents]);

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
  };

  const getTypeIcon = (type) => {
    const icons = {
      flood: '🌊',
      fire: '🔥',
      earthquake: '🏚️',
      storm: '⛈️',
      accident: '🚗',
      medical: '🏥',
      other: '⚠️'
    };
    return icons[type] || '⚠️';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#10b981',
      medium: '#f59e0b',
      high: '#ef4444',
      critical: '#dc2626'
    };
    return colors[severity] || '#6b7280';
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: { text: 'Pending', color: '#f59e0b' },
      verified: { text: 'Verified', color: '#10b981' },
      'in-progress': { text: 'In Progress', color: '#3b82f6' },
      resolved: { text: 'Resolved', color: '#6b7280' }
    };
    return badges[status] || badges.pending;
  };

  return (
    <div className="incident-list-page">
      <div className="page-header">
        <div className="header-content">
          <h1>📋 Incident Reports</h1>
          <p>Browse and monitor active incidents in your area</p>
        </div>
        <a href="/" className="back-button">← Back to Home</a>
      </div>

      <div className="content-wrapper">
        {/* Filters */}
        <div className="filters-section">
          <div className="filter-group">
            <label>Search</label>
            <input
              type="text"
              placeholder="Search incidents..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="search-input"
            />
          </div>

          <div className="filter-group">
            <label>Type</label>
            <select
              value={filters.type}
              onChange={(e) => handleFilterChange('type', e.target.value)}
              className="filter-select"
            >
              <option value="all">All Types</option>
              <option value="flood">🌊 Flood</option>
              <option value="fire">🔥 Fire</option>
              <option value="earthquake">🏚️ Earthquake</option>
              <option value="storm">⛈️ Storm</option>
              <option value="accident">🚗 Accident</option>
              <option value="medical">🏥 Medical</option>
              <option value="other">⚠️ Other</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Severity</label>
            <select
              value={filters.severity}
              onChange={(e) => handleFilterChange('severity', e.target.value)}
              className="filter-select"
            >
              <option value="all">All Levels</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Status</label>
            <select
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="filter-select"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="verified">Verified</option>
              <option value="in-progress">In Progress</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
        </div>

        {/* Stats */}
        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-number">{filteredIncidents.length}</div>
            <div className="stat-label">Active Incidents</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">
              {filteredIncidents.filter(i => i.severity === 'critical').length}
            </div>
            <div className="stat-label">Critical</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">
              {filteredIncidents.reduce((sum, i) => sum + i.affectedCount, 0)}
            </div>
            <div className="stat-label">People Affected</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">
              {filteredIncidents.filter(i => i.status === 'in-progress').length}
            </div>
            <div className="stat-label">In Progress</div>
          </div>
        </div>

        {/* Incident Cards */}
        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading incidents...</p>
          </div>
        ) : filteredIncidents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>No incidents found</h3>
            <p>Try adjusting your filters or search terms</p>
          </div>
        ) : (
          <div className="incidents-grid">
            {filteredIncidents.map(incident => (
              <div
                key={incident.id}
                className="incident-card"
                onClick={() => setSelectedIncident(incident)}
              >
                <div className="card-header">
                  <div className="type-badge">
                    <span className="type-icon">{getTypeIcon(incident.type)}</span>
                    <span className="type-text">{incident.type}</span>
                  </div>
                  <div
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(incident.severity) }}
                  >
                    {incident.severity}
                  </div>
                </div>

                <h3 className="incident-title">{incident.title}</h3>
                <p className="incident-description">{incident.description}</p>

                <div className="incident-meta">
                  <div className="meta-item">
                    <span className="meta-icon">📍</span>
                    <span className="meta-text">{incident.location.address}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-icon">👤</span>
                    <span className="meta-text">
                      {incident.reporter.name}
                      {incident.reporter.verified && <span className="verified-badge">✓</span>}
                    </span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-icon">👥</span>
                    <span className="meta-text">{incident.affectedCount} affected</span>
                  </div>
                </div>

                <div className="card-footer">
                  <span
                    className="status-badge"
                    style={{ backgroundColor: getStatusBadge(incident.status).color }}
                  >
                    {getStatusBadge(incident.status).text}
                  </span>
                  <span className="timestamp">{incident.createdAt}</span>
                  <span className="upvotes">👍 {incident.upvotes}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal for incident details */}
      {selectedIncident && (
        <div className="modal-overlay" onClick={() => setSelectedIncident(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedIncident(null)}>✕</button>

            <div className="modal-header">
              <h2>{getTypeIcon(selectedIncident.type)} {selectedIncident.title}</h2>
              <div
                className="severity-badge large"
                style={{ backgroundColor: getSeverityColor(selectedIncident.severity) }}
              >
                {selectedIncident.severity}
              </div>
            </div>

            <div className="modal-body">
              <div className="detail-section">
                <h4>Description</h4>
                <p>{selectedIncident.description}</p>
              </div>

              <div className="detail-section">
                <h4>Location</h4>
                <p>📍 {selectedIncident.location.address}</p>
                <p className="coordinates">
                  Coordinates: {selectedIncident.location.coordinates[0]}, {selectedIncident.location.coordinates[1]}
                </p>
              </div>

              <div className="detail-section">
                <h4>Reporter</h4>
                <p>
                  {selectedIncident.reporter.name}
                  {selectedIncident.reporter.verified && <span className="verified-badge">✓ Verified</span>}
                </p>
              </div>

              <div className="detail-row">
                <div className="detail-section">
                  <h4>People Affected</h4>
                  <p>{selectedIncident.affectedCount}</p>
                </div>
                <div className="detail-section">
                  <h4>Status</h4>
                  <p>{getStatusBadge(selectedIncident.status).text}</p>
                </div>
                <div className="detail-section">
                  <h4>Reported</h4>
                  <p>{selectedIncident.createdAt}</p>
                </div>
              </div>

              {selectedIncident.images.length > 0 && (
                <div className="detail-section">
                  <h4>Images</h4>
                  <div className="image-gallery">
                    {selectedIncident.images.map((img, index) => (
                      <div key={index} className="image-placeholder">
                        📷 {img}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="modal-actions">
                <button className="action-btn primary">👍 Upvote</button>
                <button className="action-btn">💬 Add Update</button>
                <button className="action-btn">📤 Share</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default IncidentList;
'''

    # pages/IncidentList.css
    incident_list_css = '''.incident-list-page {
  min-height: 100vh;
  background: #f9fafb;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.header-content p {
  opacity: 0.9;
  font-size: 1.1rem;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid white;
}

.back-button:hover {
  background: white;
  color: #667eea;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
}

.filter-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 600;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f4f6;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6b7280;
}

.incidents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.incident-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.incident-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.type-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f3f4f6;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.type-icon {
  font-size: 1.2rem;
}

.type-text {
  font-weight: 600;
  color: #374151;
  text-transform: capitalize;
}

.severity-badge {
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
}

.severity-badge.large {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
}

.incident-title {
  font-size: 1.2rem;
  color: #1f2937;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.incident-description {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.incident-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #6b7280;
}

.meta-icon {
  font-size: 1rem;
}

.verified-badge {
  display: inline-block;
  background: #10b981;
  color: white;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
  font-size: 0.75rem;
  margin-left: 0.3rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  font-size: 0.85rem;
}

.status-badge {
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.8rem;
}

.timestamp {
  color: #9ca3af;
}

.upvotes {
  color: #6b7280;
  font-weight: 600;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: slideUp 0.3s ease;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #f3f4f6;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.modal-close:hover {
  background: #e5e7eb;
  transform: rotate(90deg);
}

.modal-header {
  padding: 2rem;
  border-bottom: 2px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.modal-header h2 {
  font-size: 1.8rem;
  color: #1f2937;
  flex: 1;
}

.modal-body {
  padding: 2rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  color: #374151;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.detail-section p {
  color: #6b7280;
  line-height: 1.6;
}

.coordinates {
  font-size: 0.9rem;
  color: #9ca3af;
  margin-top: 0.25rem;
}

.detail-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.image-placeholder {
  background: #f3f4f6;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  color: #6b7280;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f3f4f6;
}

.action-btn {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #f9fafb;
  border-color: #667eea;
  color: #667eea;
}

.action-btn.primary {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.action-btn.primary:hover {
  background: #5568d3;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .filters-section {
    grid-template-columns: 1fr 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .header-content h1 {
    font-size: 2rem;
  }

  .filters-section {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .incidents-grid {
    grid-template-columns: 1fr;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }
}
'''

    # Update App.jsx to add the new route
    updated_app_jsx = '''import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import ReportIncident from './pages/ReportIncident';
import IncidentList from './pages/IncidentList';

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

            <div className="feature-card">
    <div className="icon">📢</div>
                  <h3>Emergency Alerts</h3>
                  <p>Get notified about critical situations near you</p>
                </div>
              </div>

              <div className="cta-buttons">
                <Link to="/report" className="cta-button primary">Report Now</Link>
                <Link to="/incidents" className="cta-button secondary">Browse Incidents</Link>
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
          </Routes>
        </Router>
      );
    }

    export default App;
    '''

    # Ensure the pages directory exists
    pages_path = os.path.join(frontend_path, 'pages')
    if not os.path.exists(pages_path):
        os.makedirs(pages_path)

    # Write IncidentList.jsx
    with open(os.path.join(pages_path, 'IncidentList.jsx'), 'w', encoding='utf-8') as f:
        f.write(incident_list_page)
    print("✅ Created frontend/src/pages/IncidentList.jsx")

    # Write IncidentList.css
    with open(os.path.join(pages_path, 'IncidentList.css'), 'w', encoding='utf-8') as f:
        f.write(incident_list_css)
    print("✅ Created frontend/src/pages/IncidentList.css")

    # Write App.jsx
    with open(os.path.join(frontend_path, 'App.jsx'), 'w', encoding='utf-8') as f:
        f.write(updated_app_jsx)
    print("✅ Updated frontend/src/App.jsx")

    print("\nIncident List feature created successfully!")
    print("Don't forget to restart your React server to see the changes.")


if __name__ == "__main__":
    create_incident_list_files()