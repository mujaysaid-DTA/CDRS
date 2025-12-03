const express = require('express');
const router = express.Router();
const { getResources, createResource, updateResourceStatus } = require('../controllers/resourceController');

router.get('/', getResources);
router.post('/', createResource);
router.patch('/:id', updateResourceStatus); // New route for updates

module.exports = router;
