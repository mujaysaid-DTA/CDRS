import React from 'react';
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
