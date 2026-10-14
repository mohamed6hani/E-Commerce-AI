const express = require('express');
const aiController = require('../controllers/aiController');

const router = express.Router();

router.get('/recommend', aiController.getRecommendedProducts);
router.get('/price', aiController.getDynamicPrice);

module.exports = router;