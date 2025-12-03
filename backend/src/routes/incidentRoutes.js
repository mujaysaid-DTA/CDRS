const express = require('express');
const router = express.Router();
const { getIncidents, createIncident, verifyIncident, deleteIncident } = require('../controllers/incidentController');

router.get('/', getIncidents);
router.post('/', createIncident);
router.patch('/:id/verify', verifyIncident); // Admin: Trust
router.delete('/:id', deleteIncident);       // Admin: Ban

module.exports = router;
