import React, { useState } from 'react';
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
