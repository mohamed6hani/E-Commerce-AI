import React, { useEffect, useState } from 'react';

export default function AiInsights() {
  const [recommendations, setRecommendations] = useState([]);
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ productId: '', demandFactor: '0.5', competitorPrice: '0' });
  const [priceResult, setPriceResult] = useState('');

  useEffect(() => {
    fetch('/api/ai/recommend?count=4')
      .then((res) => res.json())
      .then((data) => setRecommendations(data))
      .catch(() => setRecommendations([]));

    fetch('/api/products')
      .then((res) => res.json())
      .then((data) => setProducts(data));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handlePrice = (e) => {
    e.preventDefault();
    if (!form.productId) {
      setPriceResult('Pick a product');
      return;
    }
    const params = new URLSearchParams({
      productId: form.productId,
      demandFactor: form.demandFactor,
      competitorPrice: form.competitorPrice,
    });
    fetch(`/api/ai/price?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setPriceResult(data.error);
        } else {
          setPriceResult(`Dynamic price: $${Number(data.dynamicPrice || 0).toFixed(2)}`);
        }
      })
      .catch(() => setPriceResult('Something went wrong.'));
  };

  return (
    <div className="page-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">AI Studio</p>
          <h1>Intelligence tools</h1>
          <p>Request recommendations and run the dynamic pricing model.</p>
        </div>
      </header>
      <section className="panel">
        <h3>Recommended products</h3>
        {recommendations.length ? (
          <div className="recommend-grid">
            {recommendations.map((p) => (
              <article key={p.id || p._id}>
                <h4>{p.title}</h4>
                <p>{p.description || 'AI suggested item'}</p>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">Need at least one product before AI can respond.</p>
        )}
      </section>
      <section className="panel">
        <h3>Dynamic pricing sandbox</h3>
        <form className="price-form" onSubmit={handlePrice}>
          <select name="productId" value={form.productId} onChange={handleChange}>
            <option value="">Select product</option>
            {products.map((p) => (
              <option key={p.id || p._id} value={p.id || p._id}>
                {p.title}
              </option>
            ))}
          </select>
          <input
            name="demandFactor"
            type="number"
            step="0.1"
            min="0"
            max="2"
            value={form.demandFactor}
            onChange={handleChange}
            placeholder="Demand factor"
          />
          <input
            name="competitorPrice"
            type="number"
            step="0.01"
            value={form.competitorPrice}
            onChange={handleChange}
            placeholder="Competitor price"
          />
          <button type="submit" className="primary-btn">Run pricing</button>
        </form>
        {priceResult && <p className="status-text">{priceResult}</p>}
      </section>
    </div>
  );
}
