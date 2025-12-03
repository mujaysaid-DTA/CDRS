import os


def setup_chat_frontend():
    base_path = os.getcwd()
    pages_path = os.path.join(base_path, 'frontend', 'src', 'pages')

    print("🎨 Creating Glassmorphic Chat Interface...")

    # 1. Create Chat.jsx
    chat_jsx = """import React, { useState, useEffect, useRef } from 'react';
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
"""

    # 2. Create Chat.css (Glassmorphism)
    chat_css = """.chat-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* --- GLASS CARD CONTAINER --- */
.chat-container {
  width: 100%;
  max-width: 500px;
  height: 600px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* --- JOIN SCREEN --- */
.join-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: white;
  padding: 2rem;
  text-align: center;
}

.join-screen input {
  width: 80%;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 50px;
  border: none;
  background: rgba(0,0,0,0.3);
  color: white;
  text-align: center;
  font-size: 1.1rem;
}

.join-screen button {
  padding: 0.8rem 2rem;
  border-radius: 50px;
  border: none;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}
.join-screen button:hover { transform: scale(1.05); }

/* --- CHAT SCREEN --- */
.chat-screen {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 1.5rem;
  background: rgba(0,0,0,0.2);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-header h3 { color: white; margin: 0; }
.live-indicator { color: #10b981; font-size: 0.8rem; font-weight: bold; animation: pulse 2s infinite; }

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.chat-body {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* SCROLLBAR */
.chat-body::-webkit-scrollbar { width: 5px; }
.chat-body::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

/* MESSAGES */
.message-bubble {
  max-width: 80%;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  color: white;
  position: relative;
  word-wrap: break-word;
}

.message-bubble.me {
  align-self: flex-end;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  border-bottom-right-radius: 0;
}

.message-bubble.other {
  align-self: flex-start;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.05);
  border-bottom-left-radius: 0;
}

.msg-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  margin-top: 5px;
  opacity: 0.7;
}

.chat-footer {
  padding: 1rem;
  background: rgba(0,0,0,0.2);
  display: flex;
  gap: 10px;
}

.chat-footer input {
  flex: 1;
  padding: 0.8rem;
  border-radius: 50px;
  border: none;
  background: rgba(255,255,255,0.05);
  color: white;
  padding-left: 1.5rem;
}
.chat-footer input:focus { outline: none; background: rgba(255,255,255,0.1); }

.chat-footer button {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  background: #10b981;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
"""

    with open(os.path.join(pages_path, 'Chat.jsx'), 'w', encoding='utf-8') as f:
        f.write(chat_jsx)

    with open(os.path.join(pages_path, 'Chat.css'), 'w', encoding='utf-8') as f:
        f.write(chat_css)

    print("✅ Chat.jsx and Chat.css created.")
    print("👉 NEXT: Run 'npm install socket.io-client' inside your frontend folder.")


if __name__ == "__main__":
    setup_chat_frontend()