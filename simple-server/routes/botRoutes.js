const express = require('express');
const router = express.Router();

const botHandler = require('../handlers/botHandler');

router.get('/create', botHandler.create);
router.post('/create', botHandler.create);

module.exports = router;