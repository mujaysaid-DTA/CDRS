const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api/v1' 
  : 'https://disaster-response-system.onrender.com/api/v1';

export default API_BASE_URL;
