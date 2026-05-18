const { useState } = React;

function SettingsPanel({ config, onChange }) {
  const [open, setOpen] = useState(false);

  const handleChange = (field) => (e) => {
    onChange({ ...config, [field]: e.target.value });
  };

  return (
    <div className="settings-panel">
      <div className="settings-header" onClick={() => setOpen(!open)}>
        <span className="settings-icon">⚙️</span>
        <span className="settings-title">模型配置</span>
        <span className={`settings-arrow ${open ? 'open' : ''}`}>▼</span>
      </div>
      {open && (
        <div className="settings-body">
          <div className="settings-row">
            <label>Base URL</label>
            <input
              type="text"
              placeholder="https://api.openai.com/v1"
              value={config.baseUrl}
              onChange={handleChange('baseUrl')}
            />
          </div>
          <div className="settings-row">
            <label>API Key</label>
            <input
              type="password"
              placeholder="sk-..."
              value={config.apiKey}
              onChange={handleChange('apiKey')}
            />
          </div>
          <div className="settings-row">
            <label>Model</label>
            <input
              type="text"
              placeholder="gpt-4o"
              value={config.model}
              onChange={handleChange('model')}
            />
          </div>
        </div>
      )}
    </div>
  );
}
