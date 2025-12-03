import os


def refill_backend():
    base_path = os.getcwd()
    src_path = os.path.join(base_path, 'backend', 'src')

    print("⛽ Refilling Backend Logic...\n")

    # 1. SERVER.JS (The Entry Point)
    server_code = '''const app = require('./app');
const dotenv = require('dotenv');

dotenv.config();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`\\n🚀 Backend Server running on port ${PORT}`);
  console.log(`🔗 API URL: http://localhost:${PORT}/api/v1`);
});
'''

    # 2. APP.JS (The Configuration)
    app_code = '''const express = require('express');
const cors = require('cors');
const incidentRoutes = require('./routes/incidentRoutes');

const app = express();

// Middleware
app.use(cors()); 
app.use(express.json());

// Routes
app.use('/api/v1/incidents', incidentRoutes);

// Health Check
app.get('/', (req, res) => {
  res.send('✅ Disaster Response API is active');
});

module.exports = app;
'''

    # Write files
    files = {
        os.path.join(src_path, 'server.js'): server_code,
        os.path.join(src_path, 'app.js'): app_code
    }

    for path, content in files.items():
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Refilled: {os.path.basename(path)}")
        except Exception as e:
            print(f"❌ Error writing {path}: {e}")


if __name__ == "__main__":
    refill_backend()