import API_BASE_URL from '../config';
import React, { useState, useEffect } from 'react';
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

  // Replace the old useEffect with this:
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        setLoading(true);
        // FETCHING FROM YOUR NEW BACKEND
        const response = await fetch(`${API_BASE_URL}/incidents');
        const data = await response.json();

        setIncidents(data);
        setFilteredIncidents(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching incidents:", error);
        setLoading(false);
      }
    };

    fetchIncidents();
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
