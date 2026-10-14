const db = require('../db');

/**
 * Simple dynamic pricing algorithm implemented in JavaScript.  It mirrors
 * the logic in shared/dynamic_pricing.py: adjust price based on demand
 * factor, stock level and competitor price.
 */
function computeDynamicPrice(basePrice, demandFactor, stockLevel, competitorPrice) {
  let price = basePrice * (1 + 0.2 * demandFactor);
  if (stockLevel < 5) {
    price *= 1.1;
  }
  if (competitorPrice > 0 && price > competitorPrice) {
    price = (price + competitorPrice) / 2;
  }
  return Math.round(price * 100) / 100;
}

exports.getRecommendedProducts = async (req, res) => {
  // For demonstration purposes, return the first N products
  const countParam = parseInt(req.query.count || '5', 10);
  const count = Number.isNaN(countParam) ? 5 : Math.max(countParam, 1);
  try {
    const products = await db.all(
      'SELECT * FROM products ORDER BY created_at DESC LIMIT ?',
      [count]
    );
    res.json(products);
  } catch (err) {
    res.status(500).json({ error: 'Server error' });
  }
};

exports.getDynamicPrice = async (req, res) => {
  const { productId, demandFactor = 0.5, competitorPrice = 0 } = req.query;
  try {
    const product = await db.get('SELECT * FROM products WHERE id = ?', [productId]);
    if (!product) return res.status(404).json({ error: 'Product not found' });
    const price = computeDynamicPrice(
      product.price,
      parseFloat(demandFactor),
      product.stock,
      parseFloat(competitorPrice)
    );
    res.json({ productId, dynamicPrice: price });
  } catch (err) {
    res.status(400).json({ error: 'Invalid parameters' });
  }
};