import React, { useEffect, useState } from 'react';

export default function OrderManager() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/orders')
      .then((res) => res.json())
      .then((data) => setOrders(data))
      .catch(() => setError('Could not load orders.'));
  }, []);

  if (error) {
    return <div className="page-shell error">{error}</div>;
  }

  return (
    <div className="page-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Fulfillment</p>
          <h1>Orders</h1>
          <p>Monitor checkout activity and review order line items.</p>
        </div>
      </header>
      <section className="panel">
        {orders.length ? (
          <div className="orders-list">
            {orders.map((order) => (
              <article key={order.id || order._id}>
                <header>
                  <div>
                    <p className="eyebrow">Order #{order.id || order._id}</p>
                    <h3>${Number(order.total || 0).toFixed(2)}</h3>
                  </div>
                  <span className="pill">{order.status || 'pending'}</span>
                </header>
                <ul>
                  {(order.items || []).map((item, idx) => (
                    <li key={`${order.id}-item-${idx}`}>
                      <span>{item.product_title || item.product || 'Product'}</span>
                      <span>
                        {item.quantity} × ${Number(item.price || 0).toFixed(2)}
                      </span>
                    </li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">No orders yet.</p>
        )}
      </section>
    </div>
  );
}
