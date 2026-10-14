import React from 'react';

function SettingsPage({ theme, onThemeChange }) {
  const [selectedTheme, setSelectedTheme] = React.useState(theme);

  React.useEffect(() => {
    setSelectedTheme(theme);
  }, [theme]);

  const handleTheme = (value) => {
    setSelectedTheme(value);
    onThemeChange(value);
  };

  return (
    <div className="page-shell settings-page">
      <header className="settings-header">
        <p className="eyebrow">Control center</p>
        <h1>Settings</h1>
        <p className="muted">Fine-tune how eCommerce AI looks and behaves.</p>
      </header>

      <section className="settings-panel">
        <h2>Preferences</h2>
        <div className="settings-row">
          <div className="settings-copy">
            <p className="settings-label">Appearance</p>
            <p className="muted">Choose the default theme for dashboards and admin tools.</p>
          </div>
          <div className="appearance-options">
            <button
              type="button"
              className={selectedTheme === 'light' ? 'option-pill active' : 'option-pill'}
              onClick={() => handleTheme('light')}
            >
              Light mode
            </button>
            <button
              type="button"
              className={selectedTheme === 'dark' ? 'option-pill active' : 'option-pill'}
              onClick={() => handleTheme('dark')}
            >
              Dark mode
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default SettingsPage;
