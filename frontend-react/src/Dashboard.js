import React, { useEffect, useState } from 'react';

export default function Dashboard() {
  const [metrics, setMetrics] = useState({ products: 0, orders: 0, revenue: 0 });
  const [recentProducts, setRecentProducts] = useState([]);
  const [recentOrders, setRecentOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [productsRes, ordersRes] = await Promise.all([
          fetch('/api/products'),
          fetch('/api/orders'),
        ]);
        const products = await productsRes.json();
        const orders = await ordersRes.json();
        const revenue = orders.reduce((sum, order) => sum + Number(order.total || 0), 0);
        setMetrics({ products: products.length, orders: orders.length, revenue });
        setRecentProducts(products.slice(0, 4));
        setRecentOrders(orders.slice(0, 4));
      } catch (err) {
        setError('Unable to load dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="page-shell">Loading dashboard…</div>;
  }

  if (error) {
    return <div className="page-shell error">{error}</div>;
  }

  return (
    <div className="page-shell">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Control Room</p>
          <h1>Commerce intelligence</h1>
          <p>Monitor conversions, inventory, and AI-powered signals across your stack.</p>
          <div className="hero-chips">
            <span>Realtime metrics</span>
            <span>AI insights</span>
            <span>Admin overrides</span>
          </div>
        </div>
        <div className="hero-stats">
          <div>
            <p>Conversion rate</p>
            <strong>3.4%</strong>
          </div>
          <div>
            <p>Avg. order value</p>
            <strong>${(metrics.orders ? metrics.revenue / metrics.orders : 0).toFixed(2)}</strong>
          </div>
          <div>
            <p>Inventory coverage</p>
            <strong>{metrics.products ? '98%' : '—'}</strong>
          </div>
        </div>
      </section>
      <section className="stat-grid">
        <article className="stat-card">
          <p>Total products</p>
          <h2>{metrics.products}</h2>
        </article>
        <article className="stat-card">
          <p>Orders</p>
          <h2>{metrics.orders}</h2>
        </article>
        <article className="stat-card">
          <p>Gross revenue</p>
          <h2>${metrics.revenue.toFixed(2)}</h2>
        </article>
      </section>
      <section className="panel market-panel">
        <div className="market-chart">
          {[...Array(12)].map((_, idx) => (
            <span key={idx} style={{ height: `${20 + Math.random() * 60}%` }} />
          ))}
        </div>
        <div className="market-copy">
          <h3>Marketplace pulse</h3>
          <p>
            Pulse data simulates the latest 12h of performance so you can preview the dashboard layout
            before real traffic arrives. Hook this panel up to analytics or forecasting endpoints to
            activate it.
          </p>
        </div>
      </section>
      <div className="split-panels">
        <section className="panel">
          <h3>Recently added products</h3>
          {recentProducts.length ? (
            <ul>
              {recentProducts.map((p) => (
                <li key={p.id || p._id}>
                  <div>
                    <strong>{p.title}</strong>
                    <p className="muted-line">{p.category || 'General'}</p>
                  </div>
                  <span>${Number(p.price || 0).toFixed(2)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">No products yet</p>
          )}
        </section>
        <section className="panel">
          <h3>Latest orders</h3>
          {recentOrders.length ? (
            <ul>
              {recentOrders.map((order) => (
                <li key={order.id || order._id}>
                  <div>
                    <strong>Order #{order.id || order._id}</strong>
                    <p className="muted-line">{order.items?.length || 0} items</p>
                  </div>
                  <span>${Number(order.total || 0).toFixed(2)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">No orders yet</p>
          )}
        </section>
      </div>
    </div>
  );
}
