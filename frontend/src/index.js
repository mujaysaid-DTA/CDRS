import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';

// --- THE FIX IS HERE ---
// We changed "./IncidentList" to "./pages/IncidentList"
import IncidentList from './pages/IncidentList';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <IncidentList />
    </BrowserRouter>
  </React.StrictMode>
);