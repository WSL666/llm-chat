const { useEffect, useRef } = React;

function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'}`}>
      <div className="avatar">
        {isUser ? '🧑' : '🤖'}
      </div>
      <div className={`bubble ${isUser ? 'bubble-user' : 'bubble-assistant'}`}>
        {message.content || (
          <span className="typing-indicator">
            <span></span><span></span><span></span>
          </span>
        )}
      </div>
    </div>
  );
}

function MessageList({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.length === 0 && (
        <div className="empty-hint">
          <div className="empty-icon">💬</div>
          <p>配置好模型后，开始对话吧！</p>
        </div>
      )}
      {messages.map((msg, idx) => (
        <MessageBubble key={idx} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
