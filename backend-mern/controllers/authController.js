const db = require('../db');

const mapUser = (row) => {
  if (!row) return null;
  return {
    id: row.id,
    name: row.name,
    email: row.email,
    isAdmin: Boolean(row.is_admin),
    created_at: row.created_at,
  };
};

exports.register = async (req, res) => {
  const { name, email, password, isAdmin = false } = req.body;
  if (!name || !email || !password) {
    return res.status(400).json({ error: 'name, email and password are required' });
  }

  try {
    const existing = await db.get('SELECT id FROM users WHERE email = ?', [email]);
    if (existing) return res.status(400).json({ error: 'Email already registered' });

    const result = await db.run(
      'INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)',
      [name, email, password, isAdmin ? 1 : 0]
    );
    const user = await db.get('SELECT * FROM users WHERE id = ?', [result.lastID]);
    res.status(201).json(mapUser(user));
  } catch (err) {
    res.status(400).json({ error: 'Invalid data', details: err.message });
  }
};

exports.login = async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'email and password are required' });
  }

  try {
    const user = await db.get(
      'SELECT * FROM users WHERE email = ? AND password = ?',
      [email, password]
    );
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });
    res.json({ message: 'Login successful', user: mapUser(user) });
  } catch (err) {
    res.status(500).json({ error: 'Server error' });
  }
};