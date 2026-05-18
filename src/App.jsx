const { useState: useStateApp, useCallback } = React;

async function streamChat(config, messages, onChunk, onDone, onError) {
  const url = `${config.baseUrl.replace(/\/$/, '')}/chat/completions`;
  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`,
      },
      body: JSON.stringify({
        model: config.model,
        messages: messages.map(({ role, content }) => ({ role, content })),
        stream: true,
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      onError(`HTTP ${resp.status}: ${errText}`);
      return;
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed === 'data: [DONE]') continue;
        if (trimmed.startsWith('data: ')) {
          try {
            const json = JSON.parse(trimmed.slice(6));
            const delta = json.choices?.[0]?.delta?.content;
            if (delta) onChunk(delta);
          } catch (_) {}
        }
      }
    }
    onDone();
  } catch (err) {
    onError(err.message || String(err));
  }
}

function App() {
  const [config, setConfig] = useStateApp({
    baseUrl: '',
    apiKey: '',
    model: '',
  });
  const [messages, setMessages] = useStateApp([]);
  const [loading, setLoading] = useStateApp(false);
  const [error, setError] = useStateApp('');

  const handleSend = useCallback(async (text) => {
    if (!config.baseUrl || !config.apiKey || !config.model) {
      setError('请先在上方配置 Base URL、API Key 和 Model');
      return;
    }
    setError('');
    const userMsg = { role: 'user', content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setLoading(true);

    const assistantPlaceholder = { role: 'assistant', content: '' };
    setMessages([...newMessages, assistantPlaceholder]);

    let fullContent = '';

    await streamChat(
      config,
      newMessages,
      (chunk) => {
        fullContent += chunk;
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = { role: 'assistant', content: fullContent };
          return updated;
        });
      },
      () => {
        setLoading(false);
      },
      (errMsg) => {
        setError(errMsg);
        setLoading(false);
        setMessages((prev) => prev.slice(0, -1));
      }
    );
  }, [config, messages]);

  const handleClear = () => {
    setMessages([]);
    setError('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">🤖 LLM Chat</h1>
        {messages.length > 0 && (
          <button className="clear-btn" onClick={handleClear}>清空对话</button>
        )}
      </header>
      <SettingsPanel config={config} onChange={setConfig} />
      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError('')}>×</button>
        </div>
      )}
      <MessageList messages={messages} />
      <InputBar onSend={handleSend} loading={loading} />
    </div>
  );
}
