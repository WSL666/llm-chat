const { useState: useStateInput, useRef: useRefInput } = React;

function InputBar({ onSend, loading }) {
  const [text, setText] = useStateInput('');
  const textareaRef = useRefInput(null);

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;
    onSend(trimmed);
    setText('');
    textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e) => {
    setText(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px';
  };

  return (
    <div className="input-bar">
      <textarea
        ref={textareaRef}
        className="input-textarea"
        placeholder="输入消息，Enter 发送，Shift+Enter 换行..."
        value={text}
        onInput={handleInput}
        onKeyDown={handleKeyDown}
        onChange={(e) => setText(e.target.value)}
        rows={1}
        disabled={loading}
      />
      <button
        className={`send-btn ${loading ? 'loading' : ''}`}
        onClick={handleSend}
        disabled={loading || !text.trim()}
      >
        {loading ? '⏳' : '发送'}
      </button>
    </div>
  );
}
