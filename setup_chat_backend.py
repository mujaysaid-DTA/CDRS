import os


def setup_chat_backend():
    base_path = os.getcwd()
    backend_path = os.path.join(base_path, 'backend')
    server_path = os.path.join(backend_path, 'src', 'server.js')

    print("🔌 Upgrading Backend for Real-Time Chat...")

    # 1. Update server.js to include Socket.io and JSON storage
    server_code = """const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const http = require('http'); // Required for Socket.io
const { Server } = require('socket.io'); // The Socket.io library

const app = express();
const PORT = process.env.PORT || 5000;

// Create HTTP server (wraps Express)
const server = http.createServer(app);

// Initialize Socket.io with CORS enabled
const io = new Server(server, {
  cors: {
    origin: "*", // Allow all connections (Frontend)
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());

// --- DATABASE (JSON FILES) ---
const DATA_DIR = path.join(__dirname, '../data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR);

const INCIDENTS_FILE = path.join(DATA_DIR, 'incidents.json');
const CHAT_FILE = path.join(DATA_DIR, 'chat_history.json');

// Helper: Read Data
const readData = (file) => {
  if (!fs.existsSync(file)) return [];
  return JSON.parse(fs.readFileSync(file));
};

// Helper: Write Data
const writeData = (file, data) => {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
};

// --- REAL-TIME CHAT LOGIC ---
io.on('connection', (socket) => {
  console.log('⚡ A user connected:', socket.id);

  // 1. Send existing chat history to the new user immediately
  const history = readData(CHAT_FILE);
  socket.emit('load_history', history);

  // 2. Listen for new messages
  socket.on('send_message', (data) => {
    // data = { user: "Name", text: "Hello", time: "10:00 AM" }

    // Save to JSON file
    const currentChat = readData(CHAT_FILE);
    currentChat.push(data);

    // Keep only last 50 messages to prevent file from getting too big
    if (currentChat.length > 50) currentChat.shift();

    writeData(CHAT_FILE, currentChat);

    // Broadcast to EVERYONE (including sender)
    io.emit('receive_message', data);
  });

  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

// --- REST API ROUTES ---

// Get Incidents
app.get('/api/v1/incidents', (req, res) => {
  const incidents = readData(INCIDENTS_FILE);
  res.json(incidents);
});

// Post Incident
app.post('/api/v1/incidents', (req, res) => {
  const incidents = readData(INCIDENTS_FILE);
  const newIncident = { id: Date.now(), ...req.body, status: 'Open' };
  incidents.push(newIncident);
  writeData(INCIDENTS_FILE, incidents);

  // Real-time alert for new incident (Bonus!)
  io.emit('new_incident_alert', newIncident);

  res.status(201).json(newIncident);
});

// Start Server (Use 'server.listen' instead of 'app.listen')
server.listen(PORT, () => {
  console.log(`✅ Server is running on port ${PORT}`);
  console.log(`💬 Real-time Chat System Active`);
});
"""

    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(server_code)

    print("✅ server.js updated (Socket.io added).")
    print("👉 NEXT: Run 'npm install socket.io' inside your backend folder.")


if __name__ == "__main__":
    setup_chat_backend()