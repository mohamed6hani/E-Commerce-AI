const express = require('express');
const authController = require('../controllers/authController');

const router = express.Router();

// User registration and login routes
router.post('/register', authController.register);
router.post('/login', authController.login);

module.exports = router;