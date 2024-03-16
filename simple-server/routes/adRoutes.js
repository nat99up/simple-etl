const express = require('express');
const router = express.Router();

const adHandler = require('../handlers/adHandler');

router.get('/view', adHandler.view);
router.get('/impression', adHandler.impression);
router.get('/click', adHandler.click);

router.post('/view', adHandler.view);
router.post('/impression', adHandler.impression);
router.post('/click', adHandler.click);

module.exports = router;