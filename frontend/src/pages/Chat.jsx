import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import API_BASE_URL from '../config';
import './Chat.css';

// Extract the domain only for socket connection (remove /api/v1)
const SOCKET_URL = API_BASE_URL.replace('/api/v1', '');
const socket = io(SOCKET_URL);

function Chat() {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [username, setUsername] = useState("");
  const [isJoined, setIsJoined] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Listen for incoming messages
    socket.on('receive_message', (data) => {
      setMessages((prev) => [...prev, data]);
    });

    // Load history when joining
    socket.on('load_history', (history) => {
      setMessages(history);
    });

    // Cleanup listener on unmount
    return () => {
      socket.off('receive_message');
      socket.off('load_history');
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const joinChat = () => {
    if (username !== "") {
      setIsJoined(true);
    }
  };

  const sendMessage = async () => {
    if (currentMessage !== "") {
      const messageData = {
        user: username,
        text: currentMessage,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      await socket.emit('send_message', messageData);
      setCurrentMessage("");
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        {!isJoined ? (
          <div className="join-screen">
            <h2>⛑️ Volunteer Chat</h2>
            <p>Enter your name to join the coordination channel.</p>
            <input 
              type="text" 
              placeholder="Your Name..." 
              onChange={(event) => setUsername(event.target.value)} 
            />
            <button onClick={joinChat}>Join Room</button>
          </div>
        ) : (
          <div className="chat-screen">
            <div className="chat-header">
              <h3>📡 Live Coordination</h3>
              <span className="live-indicator">● Live</span>
            </div>

            <div className="chat-body">
              {messages.map((msg, index) => (
                <div 
                  className={`message-bubble ${msg.user === username ? "me" : "other"}`} 
                  key={index}
                >
                  <div className="msg-content">
                    <p>{msg.text}</p>
                  </div>
                  <div className="msg-meta">
                    <span id="author">{msg.user}</span>
                    <span id="time">{msg.time}</span>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className="chat-footer">
              <input 
                type="text" 
                value={currentMessage}
                placeholder="Type a message..." 
                onChange={(event) => setCurrentMessage(event.target.value)}
                onKeyPress={(event) => event.key === 'Enter' && sendMessage()}
              />
              <button onClick={sendMessage}>➤</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;
