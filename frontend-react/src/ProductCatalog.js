import React, { useEffect, useState } from 'react';

export default function ProductCatalog() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="catalog-page">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Intelligence</p>
          <h1>Product Catalog</h1>
          <p>Live inventory connected to the AI pricing engine.</p>
        </div>
        <span className="catalog-count">{products.length} products</span>
      </header>
      <section className="product-grid">
        {products.map((p) => (
          <article key={p._id || p.id} className="product-card">
            <div className="product-meta">
              <h2>{p.title}</h2>
              <p>{p.description || 'No description available yet.'}</p>
            </div>
            <dl>
              <div>
                <dt>Price</dt>
                <dd>${Number(p.price || 0).toFixed(2)}</dd>
              </div>
              <div>
                <dt>Stock</dt>
                <dd>{p.stock ?? '—'}</dd>
              </div>
              <div>
                <dt>Category</dt>
                <dd>{p.category || 'General'}</dd>
              </div>
            </dl>
          </article>
        ))}
        {!products.length && (
          <div className="empty-state">
            <h3>No products yet</h3>
            <p>Add products through the API to see them appear here in real time.</p>
          </div>
        )}
      </section>
    </div>
  );
}
