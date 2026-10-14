const db = require('../db');

const pickProduct = (row) => {
  if (!row) return null;
  return {
    id: row.id,
    title: row.title,
    description: row.description,
    category: row.category,
    price: row.price,
    stock: row.stock,
    image_url: row.image_url,
    created_at: row.created_at,
    updated_at: row.updated_at,
  };
};

exports.getProducts = async (req, res) => {
  try {
    const products = await db.all('SELECT * FROM products ORDER BY created_at DESC');
    res.json(products.map(pickProduct));
  } catch (err) {
    res.status(500).json({ error: 'Server error' });
  }
};

exports.createProduct = async (req, res) => {
  const { title, price, stock } = req.body;
  if (!title || price === undefined || stock === undefined) {
    return res.status(400).json({ error: 'title, price and stock are required' });
  }

  const description = req.body.description || '';
  const category = req.body.category || '';
  const imageUrl = req.body.image_url || '';

  try {
    const result = await db.run(
      `INSERT INTO products (title, description, category, price, stock, image_url)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [title, description, category, Number(price), Number(stock), imageUrl]
    );
    const product = await db.get('SELECT * FROM products WHERE id = ?', [result.lastID]);
    res.status(201).json(pickProduct(product));
  } catch (err) {
    res.status(400).json({ error: 'Invalid data', details: err.message });
  }
};

exports.getProductById = async (req, res) => {
  try {
    const product = await db.get('SELECT * FROM products WHERE id = ?', [req.params.id]);
    if (!product) return res.status(404).json({ error: 'Not found' });
    res.json(pickProduct(product));
  } catch (err) {
    res.status(400).json({ error: 'Invalid ID' });
  }
};

exports.updateProduct = async (req, res) => {
  const allowed = ['title', 'description', 'category', 'price', 'stock', 'image_url'];
  const fields = [];
  const values = [];

  allowed.forEach((field) => {
    if (req.body[field] !== undefined) {
      fields.push(`${field} = ?`);
      const numericFields = ['price', 'stock'];
      const value = numericFields.includes(field) ? Number(req.body[field]) : req.body[field];
      values.push(value);
    }
  });

  if (!fields.length) {
    return res.status(400).json({ error: 'No valid fields supplied' });
  }

  values.push(req.params.id);

  try {
    const result = await db.run(
      `UPDATE products SET ${fields.join(', ')}, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      values
    );
    if (!result.changes) return res.status(404).json({ error: 'Not found' });
    const product = await db.get('SELECT * FROM products WHERE id = ?', [req.params.id]);
    res.json(pickProduct(product));
  } catch (err) {
    res.status(400).json({ error: 'Invalid data', details: err.message });
  }
};

exports.deleteProduct = async (req, res) => {
  try {
    const result = await db.run('DELETE FROM products WHERE id = ?', [req.params.id]);
    if (!result.changes) return res.status(404).json({ error: 'Not found' });
    res.json({ message: 'Deleted' });
  } catch (err) {
    res.status(400).json({ error: 'Invalid ID' });
  }
};