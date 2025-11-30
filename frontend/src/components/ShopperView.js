import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ShopperView = () => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { sender: 'bot', text: "Hi! I'm your AI shopping assistant. Looking for something specific?" }
  ]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMsg = { sender: 'user', text: query };
    setChatHistory(prev => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const res = await axios.post('/api/chat/query', {
        user_id: 'guest',
        text: userMsg.text
      });

      const botMsg = {
        sender: 'bot',
        text: res.data.response_text,
        data: res.data.data,
        action: res.data.action
      };
      setChatHistory(prev => [...prev, botMsg]);
    } catch (error) {
      console.error("Error sending message:", error);
      setChatHistory(prev => [...prev, { sender: 'bot', text: "Sorry, I'm having trouble connecting right now." }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="glass-card" style={{ height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <div className="chat-window" style={{ flex: 1, overflowY: 'auto', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`message ${msg.sender}`}
            style={{
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '80%',
              padding: '12px 16px',
              borderRadius: '16px',
              borderBottomRightRadius: msg.sender === 'user' ? '4px' : '16px',
              borderBottomLeftRadius: msg.sender === 'bot' ? '4px' : '16px',
              background: msg.sender === 'user' ? 'var(--primary)' : 'rgba(255,255,255,0.1)',
              color: 'white',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}
          >
            <p style={{ margin: 0 }}>{msg.text}</p>

            {/* Render Product Cards if available */}
            {msg.data && Array.isArray(msg.data) && msg.data.length > 0 && (
              <div className="product-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '10px', marginTop: '10px' }}>
                {msg.data.map((item, i) => (
                  <div key={i} style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px' }}>
                    <div style={{ height: '80px', background: '#334155', borderRadius: '6px', marginBottom: '8px' }}></div>
                    <strong style={{ display: 'block', fontSize: '0.9rem' }}>{item.name}</strong>
                    <span style={{ color: 'var(--accent)', fontSize: '0.85rem' }}>₹{item.price}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="message bot" style={{ alignSelf: 'flex-start', background: 'rgba(255,255,255,0.1)', padding: '12px', borderRadius: '16px' }}>
            <span className="typing-dot">...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area" style={{ display: 'flex', gap: '10px', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <input
          type="text"
          className="input-field"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask for products, stores, or recommendations..."
        />
        <button className="btn-primary" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ShopperView;