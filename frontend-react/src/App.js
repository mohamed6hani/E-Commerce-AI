import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, NavLink, useNavigate, useLocation } from 'react-router-dom';
import ProductCatalog from './ProductCatalog';
import Dashboard from './Dashboard';
import ProductManager from './ProductManager';
import OrderManager from './OrderManager';
import AiInsights from './AiInsights';
import SettingsPage from './SettingsPage';
import './App.css';

function NavIcon({ name }) {
  const paths = {
    dashboard: 'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
    catalog: 'M4 7h16l-1 14H5z M8 7V5a4 4 0 0 1 8 0v2',
    inventory: 'M3 7l9-4 9 4-9 4z M3 7v10l9 4 9-4V7 M12 11v10',
    orders: 'M6 3h12v18H6z M9 8h6 M9 12h6 M9 16h4',
    ai: 'M12 3l2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z',
    settings: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8 M12 3v2 M12 19v2 M3 12h2 M19 12h2 M5.6 5.6L7 7 M17 17l1.4 1.4 M5.6 18.4L7 17 M17 7l1.4-1.4',
    signout: 'M10 4H4v16h6 M14 8l4 4-4 4 M8 12h10',
    menu: 'M4 6h16 M4 12h16 M4 18h16',
    close: 'M6 6l12 12 M18 6L6 18',
  };
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7"
      strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="nav-icon">
      <path d={paths[name]} />
    </svg>
  );
}

function AdminNav() {
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const menuButton = React.useRef(null);

  const buttons = [
    { label: 'Dashboard', path: '/dashboard', icon: 'dashboard' },
    { label: 'Catalog', path: '/products', icon: 'catalog' },
    { label: 'Manage products', path: '/admin/products', icon: 'inventory' },
    { label: 'Orders', path: '/admin/orders', icon: 'orders' },
    { label: 'AI studio', path: '/admin/ai', icon: 'ai' },
    { label: 'Settings', path: '/admin/settings', icon: 'settings' },
  ];

  React.useEffect(() => setMobileOpen(false), [location.pathname]);

  const closeMenu = React.useCallback(() => {
    setMobileOpen(false);
    menuButton.current?.focus();
  }, []);

  React.useEffect(() => {
    if (!mobileOpen) return;
    const handleEscape = (event) => {
      if (event.key === 'Escape') closeMenu();
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [mobileOpen, closeMenu]);

  const handleSignOut = () => {
    if (window.confirm('Sign out and return to the login page?')) {
      navigate('/login');
    }
  };

  return (
    <>
      <div className="mobile-toolbar">
        <button ref={menuButton} type="button" className="menu-toggle"
          aria-label="Open navigation" aria-expanded={mobileOpen} aria-controls="store-sidebar"
          onClick={() => setMobileOpen((open) => !open)}>
          <NavIcon name="menu" />
        </button>
        <span>eCommerce AI</span>
      </div>
      {mobileOpen && <button type="button" className="sidebar-scrim" aria-label="Close navigation"
        onClick={closeMenu} />}
      <aside id="store-sidebar" className={`admin-sidebar${mobileOpen ? ' is-open' : ''}`}>
        <div className="sidebar-header">
          <NavLink to="/dashboard" className="sidebar-brand" onClick={() => setMobileOpen(false)}>
            <span className="brand-mark" aria-hidden="true">e</span>
            <span><strong>eCommerce AI</strong><small>Store management</small></span>
          </NavLink>
          <button type="button" className="sidebar-close" aria-label="Close sidebar" onClick={closeMenu}>
            <NavIcon name="close" />
          </button>
        </div>
        <p className="sidebar-label">Workspace</p>
        <nav className="admin-nav" aria-label="Main navigation">
          <div className="nav-links">
            {buttons.map((btn) => (
              <NavLink key={btn.path} to={btn.path}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) => `nav-btn${isActive ? ' active' : ''}`}>
                <NavIcon name={btn.icon} />
                <span>{btn.label}</span>
              </NavLink>
            ))}
          </div>
        </nav>
        <div className="sidebar-footer">
          <button type="button" className="nav-btn signout-btn" onClick={handleSignOut}>
            <NavIcon name="signout" />
            <span>Sign out</span>
          </button>
        </div>
      </aside>
    </>
  );
}

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="app-shell">
      <div className="aurora aurora-one" />
      <div className="aurora aurora-two" />
      <form className="login-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Welcome back</p>
        <h1 className="login-heading">Log in to eCommerce AI</h1>
        <p className="login-subheading">
          Enter your credentials to access the product intelligence dashboard.
        </p>
        <label className="field">
          <span>Email</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />
        </label>
        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
        </label>
        <button type="submit" className="primary-btn">
          Sign in
        </button>
        <p className="hint-text">
          Need an account? <button type="button" className="link" onClick={() => {
            fetch('/api/users/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ name: 'Admin', email: 'admin', password: 'admin' })
            })
              .then(res => res.json())
              .then(data => {
                if (data.error) {
                  alert('Account already exists or error: ' + data.error);
                } else {
                  alert('Admin account created! You can now log in with admin/admin.');
                }
              })
              .catch(() => alert('Failed to create account.'));
          }}>Create admin/admin account</button>
        </p>
      </form>
    </div>
  );
}

function AppLayout({ theme, onThemeChange }) {
  const isLogin = useLocation().pathname === '/login';
  return (
    <div className={isLogin ? 'auth-layout' : 'workspace-layout'}>
      {!isLogin && <AdminNav />}
      <main className={isLogin ? 'auth-content' : 'workspace-content'}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/products" element={<ProductCatalog />} />
          <Route path="/admin/products" element={<ProductManager />} />
          <Route path="/admin/orders" element={<OrderManager />} />
          <Route path="/admin/ai" element={<AiInsights />} />
          <Route path="/admin/settings" element={<SettingsPage theme={theme} onThemeChange={onThemeChange} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  const getInitialTheme = () => {
    if (typeof window === 'undefined') {
      return 'light';
    }
    return localStorage.getItem('theme') || 'light';
  };

  const [theme, setTheme] = React.useState(getInitialTheme);

  React.useEffect(() => {
    if (typeof document === 'undefined') {
      return;
    }
    document.body.classList.toggle('light-mode', theme === 'light');
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  return (
    <BrowserRouter>
      <AppLayout theme={theme} onThemeChange={setTheme} />
    </BrowserRouter>
  );
}

export default App;
