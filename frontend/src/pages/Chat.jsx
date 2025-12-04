import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const Chat = ({ incidentId }) => {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false); // Controls the "..." animation
  const messagesEndRef = useRef(null);

  const [history, setHistory] = useState([
    { sender: 'System', text: `Connected to secure channel #${incidentId}` },
    { sender: 'Support', text: 'HQ here. What is the current status?' }
  ]);

  // Reset when switching incidents
  useEffect(() => {
    setHistory([
      { sender: 'System', text: `Connected to secure channel #${incidentId}` },
      { sender: 'Support', text: 'HQ here. What is the current status?' }
    ]);
    setIsTyping(false);
  }, [incidentId]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, isTyping]);

  const handleSend = () => {
    if (!message.trim()) return;

    // 1. Add User Message immediately
    const newMessage = { sender: 'You', text: message };
    setHistory((prev) => [...prev, newMessage]);
    setMessage('');

    // 2. Start "Typing" animation
    setIsTyping(true);

    // 3. Simulate delay then reply
    setTimeout(() => {
      setIsTyping(false); // Stop typing animation
      setHistory((prev) => [
        ...prev,
        { sender: 'Support', text: 'Copy that. Deploying resources to your location.' }
      ]);
    }, 2000); // 2 second delay so you can see the animation
  };

  return (
    <div className="chat-window">

      {/* Animated Header */}
      <div className="chat-header">
        <div style={{display:'flex', flexDirection:'column'}}>
          <span style={{fontSize:'1.1em'}}>Incident #{incidentId}</span>
          <span style={{fontSize:'0.8em', opacity: 0.8}}>Command Center</span>
        </div>
        <div className="status-badge">
          <div className="pulse-dot"></div>
          <span>LIVE</span>
        </div>
      </div>

      {/* Messages Area */}
      <div className="messages-list">
        {history.map((msg, index) => (
          <div
            key={index}
            className={`message-bubble ${msg.sender === 'You' ? 'sent' : 'received'}`}
          >
            {msg.sender !== 'You' && <span className="sender-label">{msg.sender}</span>}
            {msg.text}
          </div>
        ))}

        {/* Typing Indicator Animation */}
        {isTyping && (
          <div className="typing-indicator">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type emergency update..."
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="send-button" onClick={handleSend}>
          {/* Send Icon SVG */}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 2L11 13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Chat;