/*
 * Entry point for the MERN backend.  This script sets up an Express
 * server, initializes the SQLite data store and mounts routers for
 * products, users, orders and AI services.
 */

const path = require('path');
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();
require('./db');

const productRoutes = require('./routes/productRoutes');
const userRoutes = require('./routes/userRoutes');
const orderRoutes = require('./routes/orderRoutes');
const aiRoutes = require('./routes/aiRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Mount routes
app.use('/api/products', productRoutes);
app.use('/api/users', userRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/ai', aiRoutes);

// Health check stays under the API namespace to avoid clashing with frontend routes
app.get('/api/health', (req, res) => res.send('Backend running'));

// Serve the React build output (if it exists) so login UI lives on same port
const buildPath = path.join(__dirname, '..', 'frontend-react', 'build');
app.use(express.static(buildPath));
app.get('*', (req, res, next) => {
	if (req.path.startsWith('/api')) return next();
	res.sendFile(path.join(buildPath, 'index.html'));
});

const port = process.env.PORT || 8800;
app.listen(port, () => console.log(`Server running on port ${port}`));