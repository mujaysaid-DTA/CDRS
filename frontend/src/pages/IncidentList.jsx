import React, { useState } from 'react';
import Chat from './Chat';

const IncidentList = () => {
  // 1. State to track which incident is currently selected
  const [selectedIncidentId, setSelectedIncidentId] = useState(null);

  // 2. Mock Data (This simulates data coming from a database)
  const incidents = [
    { id: 101, title: "Server Down", status: "Critical" },
    { id: 102, title: "Login Issue", status: "Open" },
    { id: 103, title: "Email Delay", status: "Resolved" },
  ];

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Incident Dashboard</h1>

      <div style={{ display: 'flex', gap: '20px', border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>

        {/* LEFT SIDE: The List of Incidents */}
        <div style={{ flex: 1, borderRight: '1px solid #eee', paddingRight: '20px' }}>
          <h3>Active Incidents</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {incidents.map((incident) => (
              <li
                key={incident.id}
                style={{
                  marginBottom: '10px',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  backgroundColor: selectedIncidentId === incident.id ? '#e6f7ff' : 'white' // Highlight selected
                }}
              >
                <strong>#{incident.id} - {incident.title}</strong>
                <br />
                <span style={{ color: incident.status === 'Critical' ? 'red' : 'green', fontSize: '0.9em' }}>
                  {incident.status}
                </span>
                <br />
                <button
                  onClick={() => setSelectedIncidentId(incident.id)}
                  style={{
                    marginTop: '8px',
                    padding: '5px 10px',
                    cursor: 'pointer',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '3px'
                  }}
                >
                  Chat about this
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* RIGHT SIDE: The Chat Window */}
        <div style={{ flex: 1, paddingLeft: '20px' }}>
          {selectedIncidentId ? (
            <div>
              <h3 style={{ marginTop: 0 }}>Chat Room: Incident #{selectedIncidentId}</h3>
              {/* This renders your Chat.jsx file */}
              <Chat incidentId={selectedIncidentId} />
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#888' }}>
              <p>Select an incident on the left to start chatting.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default IncidentList;