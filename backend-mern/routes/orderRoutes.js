const express = require('express');
const db = require('../db');

const router = express.Router();

const mapOrderItems = (items, orderId) =>
  items
    .filter((item) => item.order_id === orderId)
    .map((item) => ({
      id: item.id,
      product_id: item.product_id,
      quantity: item.quantity,
      price: item.price,
      product_title: item.product_title || null,
    }));

const mapOrder = (order, items = []) => ({
  id: order.id,
  user_id: order.user_id,
  total: order.total,
  status: order.status,
  created_at: order.created_at,
  updated_at: order.updated_at,
  items: mapOrderItems(items, order.id),
});

router.get('/', async (req, res) => {
  try {
    const orders = await db.all('SELECT * FROM orders ORDER BY created_at DESC');
    if (!orders.length) return res.json([]);

    const orderIds = orders.map((o) => o.id);
    const placeholders = orderIds.map(() => '?').join(',');
    const items = await db.all(
      `SELECT order_items.*, products.title AS product_title
       FROM order_items
       LEFT JOIN products ON products.id = order_items.product_id
       WHERE order_id IN (${placeholders})`,
      orderIds
    );

    const response = orders.map((order) => mapOrder(order, items));
    res.json(response);
  } catch (err) {
    res.status(500).json({ error: 'Server error', details: err.message });
  }
});

router.post('/', async (req, res) => {
  const userId = req.body.userId;
  const items = Array.isArray(req.body.items) ? req.body.items : [];
  const status = req.body.status || 'pending';

  if (!userId || !items.length) {
    return res.status(400).json({ error: 'userId and at least one order item are required' });
  }

  const total = items.reduce((sum, item) => sum + Number(item.quantity || 0) * Number(item.price || 0), 0);

  try {
    await db.run('BEGIN TRANSACTION');
    const orderResult = await db.run('INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)', [
      userId,
      total,
      status,
    ]);

    const orderId = orderResult.lastID;
    for (const item of items) {
      if (!item.productId) {
        throw new Error('Each order item must include productId');
      }
      await db.run(
        'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
        [orderId, item.productId, Number(item.quantity || 0), Number(item.price || 0)]
      );
    }
    await db.run('COMMIT');

    const order = await db.get('SELECT * FROM orders WHERE id = ?', [orderId]);
    const orderItems = await db.all(
      `SELECT order_items.*, products.title AS product_title
       FROM order_items
       LEFT JOIN products ON products.id = order_items.product_id
       WHERE order_id = ?`,
      [orderId]
    );
    res.status(201).json(mapOrder(order, orderItems));
  } catch (err) {
    await db.run('ROLLBACK').catch(() => {});
    res.status(400).json({ error: 'Invalid data', details: err.message });
  }
});

module.exports = router;