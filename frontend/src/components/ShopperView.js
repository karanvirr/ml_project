import React, { useState } from 'react';
import axios from 'axios';

// API base URL
const API_URL = 'http://localhost:8000/api';

function ShopperView() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: "Hi! How can I help you find today?" }
  ]);
  const [input, setInput] = useState('');
  const [products, setProducts] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { from: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setProducts([]); // Clear old products

    try {
      const response = await axios.post(`${API_URL}/chat/query`, {
        user_id: 'shopper123',
        text: input,
      });

      const botResponse = response.data;
      const botMessage = { from: 'bot', text: botResponse.response_text };
      setMessages([...messages, userMessage, botMessage]);

      if (botResponse.action === 'recommend' && botResponse.data) {
        setProducts(botResponse.data);
      }
    } catch (error) {
      console.error("Error fetching chat response:", error);
      const errorMessage = { from: 'bot', text: "Oops, something went wrong. Please try again." };
      setMessages([...messages, userMessage, errorMessage]);
    }
  };

  return (
    <div className="shopper-view">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.from}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask me for products or stores..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      {products.length > 0 && (
        <div className="product-list">
          {products.map((product) => (
            <div key={product.item_id} className="product-card">
              <h3>{product.name}</h3>
              <p><strong>Price:</strong> ₹{product.price.toFixed(2)}</p>
              <p><strong>Store:</strong> {product.store_id}</p>
              <p>{product.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ShopperView;