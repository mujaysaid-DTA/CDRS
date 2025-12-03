import React from 'react';
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
