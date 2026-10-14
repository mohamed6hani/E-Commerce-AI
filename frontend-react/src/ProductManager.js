import React, { useEffect, useState } from 'react';

const emptyForm = {
  title: '',
  description: '',
  category: '',
  price: '',
  stock: '',
  image_url: '',
};

export default function ProductManager() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [status, setStatus] = useState('');

  const fetchProducts = () => {
    fetch('/api/products')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch(() => setStatus('Could not load products.'));
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleCreate = (e) => {
    e.preventDefault();
    setStatus('');
    fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        price: Number(form.price),
        stock: Number(form.stock),
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((body) => Promise.reject(body.error || 'Failed to create product'));
        }
        return res.json();
      })
      .then(() => {
        setForm(emptyForm);
        fetchProducts();
        setStatus('Product created');
      })
      .catch((err) => setStatus(typeof err === 'string' ? err : 'Could not create product.'));
  };

  const handleDelete = (id) => {
    if (!window.confirm('Delete this product?')) return;
    fetch(`/api/products/${id}`, { method: 'DELETE' })
      .then(() => fetchProducts())
      .catch(() => setStatus('Failed to delete product.'));
  };

  return (
    <div className="page-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Inventory</p>
          <h1>Manage products</h1>
          <p>Create items and keep stock in sync.</p>
        </div>
      </header>
      <section className="panel">
        <h3>Add a product</h3>
        <form className="product-form" onSubmit={handleCreate}>
          <input name="title" placeholder="Title" value={form.title} onChange={handleChange} required />
          <textarea
            name="description"
            placeholder="Description"
            value={form.description}
            onChange={handleChange}
            rows={3}
          />
          <div className="form-grid">
            <input name="category" placeholder="Category" value={form.category} onChange={handleChange} />
            <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} required />
            <input name="stock" type="number" placeholder="Stock" value={form.stock} onChange={handleChange} required />
          </div>
          <input name="image_url" placeholder="Image URL" value={form.image_url} onChange={handleChange} />
          <button type="submit" className="primary-btn">Save product</button>
          {status && <p className="status-text">{status}</p>}
        </form>
      </section>
      <section className="panel">
        <h3>Product list</h3>
        {products.length ? (
          <table className="products-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id || p._id}>
                  <td>{p.title}</td>
                  <td>{p.category || '—'}</td>
                  <td>${Number(p.price || 0).toFixed(2)}</td>
                  <td>{p.stock}</td>
                  <td>
                    <button type="button" className="danger-btn" onClick={() => handleDelete(p.id || p._id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="muted">No products yet.</p>
        )}
      </section>
    </div>
  );
}
