import os
import json


def create_project_structure():
    """
    Creates the complete file structure for the Disaster Response System with template content
    """

    # Root package.json
    root_package = {
        "name": "disaster-response-system",
        "version": "1.0.0",
        "private": True,
        "workspaces": [
            "frontend",
            "backend",
            "mobile",
            "admin-dashboard",
            "shared"
        ],
        "scripts": {
            "install:all": "npm install && cd frontend && npm install && cd ../backend && npm install && cd ../mobile && npm install && cd ../admin-dashboard && npm install",
            "dev:frontend": "cd frontend && npm start",
            "dev:backend": "cd backend && npm run dev",
            "dev:admin": "cd admin-dashboard && npm start",
            "build:all": "cd frontend && npm run build && cd ../admin-dashboard && npm run build"
        }
    }

    # Frontend package.json
    frontend_package = {
        "name": "disaster-response-frontend",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.14.0",
            "axios": "^1.4.0",
            "redux": "^4.2.1",
            "@reduxjs/toolkit": "^1.9.5",
            "react-redux": "^8.1.1",
            "leaflet": "^1.9.4",
            "react-leaflet": "^4.2.1",
            "socket.io-client": "^4.6.2",
            "date-fns": "^2.30.0",
            "formik": "^2.4.2",
            "yup": "^1.2.0",
            "react-toastify": "^9.1.3"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "devDependencies": {
            "react-scripts": "5.0.1"
        }
    }

    # Backend package.json
    backend_package = {
        "name": "disaster-response-backend",
        "version": "1.0.0",
        "main": "src/server.js",
        "scripts": {
            "start": "node src/server.js",
            "dev": "nodemon src/server.js",
            "test": "jest",
            "migrate": "node database/migrate.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.3.1",
            "socket.io": "^4.6.2",
            "bcryptjs": "^2.4.3",
            "jsonwebtoken": "^9.0.1",
            "dotenv": "^16.3.1",
            "cors": "^2.8.5",
            "helmet": "^7.0.0",
            "express-validator": "^7.0.1",
            "multer": "^1.4.5-lts.1",
            "redis": "^4.6.7",
            "nodemailer": "^6.9.3",
            "twilio": "^4.14.0",
            "firebase-admin": "^11.10.1",
            "bull": "^4.11.3",
            "winston": "^3.10.0",
            "compression": "^1.7.4",
            "express-rate-limit": "^6.8.1"
        },
        "devDependencies": {
            "nodemon": "^3.0.1",
            "jest": "^29.6.1",
            "supertest": "^6.3.3"
        }
    }

    # Mobile package.json
    mobile_package = {
        "name": "disaster-response-mobile",
        "version": "1.0.0",
        "main": "src/App.js",
        "scripts": {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web"
        },
        "dependencies": {
            "react": "18.2.0",
            "react-native": "0.72.3",
            "expo": "~49.0.0",
            "@react-navigation/native": "^6.1.7",
            "@react-navigation/stack": "^6.3.17",
            "axios": "^1.4.0",
            "react-native-maps": "1.7.1",
            "expo-location": "~16.1.0",
            "expo-camera": "~13.4.2",
            "expo-notifications": "~0.20.1",
            "socket.io-client": "^4.6.2"
        }
    }

    # Admin dashboard package.json
    admin_package = {
        "name": "disaster-response-admin",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.14.0",
            "axios": "^1.4.0",
            "recharts": "^2.7.2",
            "date-fns": "^2.30.0",
            "@mui/material": "^5.14.1",
            "@mui/icons-material": "^5.14.1",
            "@emotion/react": "^11.11.1",
            "@emotion/styled": "^11.11.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build"
        },
        "devDependencies": {
            "react-scripts": "5.0.1"
        }
    }

    # File templates
    templates = {
        '.gitignore': '''# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
build/
dist/
*.log

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Mobile
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*
.expo/
.expo-shared/

# Backend
uploads/
logs/
''',
        'README.md': '''# Disaster Response System

A comprehensive crowdsourcing platform for disaster response and resource coordination.

## Features

- Real-time incident reporting with geolocation
- Interactive disaster map with heatmaps
- Resource matching and volunteer coordination
- Multi-channel notifications (SMS, Email, Push)
- Offline-first Progressive Web App
- Admin dashboard with analytics
- Mobile apps for iOS and Android

## Tech Stack

**Frontend:** React, Redux, Leaflet Maps, Socket.io
**Backend:** Node.js, Express, MongoDB, Redis, Socket.io
**Mobile:** React Native, Expo
**Infrastructure:** Docker, Kubernetes, Nginx

## Getting Started

### Prerequisites
- Node.js 16+
- MongoDB 5+
- Redis 6+
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd disaster-response-system
```

2. Install all dependencies
```bash
npm run install:all
```

3. Configure environment variables
- Copy `.env.example` to `.env` in backend and frontend directories
- Fill in your configuration values

4. Start development servers
```bash
# Terminal 1 - Backend
npm run dev:backend

# Terminal 2 - Frontend
npm run dev:frontend

# Terminal 3 - Admin Dashboard
npm run dev:admin
```

## Project Structure

- `/frontend` - React web application
- `/backend` - Node.js API server
- `/mobile` - React Native mobile app
- `/admin-dashboard` - Admin interface
- `/shared` - Shared types and constants
- `/database` - Database migrations and seeds
- `/infrastructure` - DevOps configurations

## Documentation

See the `/docs` folder for detailed documentation:
- API Documentation
- Architecture Overview
- Deployment Guide
- User Guide

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
''',
        'backend/.env': '''# Server Configuration
NODE_ENV=development
PORT=5000
API_VERSION=v1

# Database
MONGODB_URI=mongodb://localhost:27017/disaster_response
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRE=7d

# AWS S3 (for file uploads)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_BUCKET_NAME=disaster-response-uploads

# Email Service (Nodemailer)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_email_password

# SMS Service (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Firebase (Push Notifications)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY=your_firebase_private_key
FIREBASE_CLIENT_EMAIL=your_firebase_client_email

# Geocoding API
GEOCODING_API_KEY=your_geocoding_api_key

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
''',
        'frontend/.env': '''REACT_APP_API_URL=http://localhost:5000/api/v1
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_MAP_TILE_URL=https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
''',
        'backend/src/server.js': '''const app = require('./app');
const mongoose = require('mongoose');
const { createServer } = require('http');
const { initializeSocket } = require('./websocket/socketHandler');
require('dotenv').config();

const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI;

// Create HTTP server
const httpServer = createServer(app);

// Initialize Socket.io
initializeSocket(httpServer);

// Connect to MongoDB
mongoose
  .connect(MONGODB_URI)
  .then(() => {
    console.log('✅ Connected to MongoDB');

    // Start server
    httpServer.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
      console.log(`📡 Environment: ${process.env.NODE_ENV}`);
    });
  })
  .catch((error) => {
    console.error('❌ MongoDB connection error:', error);
    process.exit(1);
  });

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('❌ Unhandled Rejection:', err);
  httpServer.close(() => process.exit(1));
});
''',
        'backend/src/app.js': '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const authRoutes = require('./routes/authRoutes');
const incidentRoutes = require('./routes/incidentRoutes');
const resourceRoutes = require('./routes/resourceRoutes');
const volunteerRoutes = require('./routes/volunteerRoutes');
const messageRoutes = require('./routes/messageRoutes');
const adminRoutes = require('./routes/adminRoutes');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000,
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100
});
app.use('/api/', limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression
app.use(compression());

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API Routes
const API_VERSION = process.env.API_VERSION || 'v1';
app.use(`/api/${API_VERSION}/auth`, authRoutes);
app.use(`/api/${API_VERSION}/incidents`, incidentRoutes);
app.use(`/api/${API_VERSION}/resources`, resourceRoutes);
app.use(`/api/${API_VERSION}/volunteers`, volunteerRoutes);
app.use(`/api/${API_VERSION}/messages`, messageRoutes);
app.use(`/api/${API_VERSION}/admin`, adminRoutes);

// Error handling middleware (must be last)
app.use(errorHandler);

module.exports = app;
''',
        'backend/src/models/User.js': '''const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\\S+@\\S+\\.\\S+$/, 'Please provide a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: 8,
    select: false
  },
  phone: {
    type: String,
    trim: true
  },
  role: {
    type: String,
    enum: ['citizen', 'volunteer', 'responder', 'admin'],
    default: 'citizen'
  },
  location: {
    type: {
      type: String,
      enum: ['Point'],
      default: 'Point'
    },
    coordinates: {
      type: [Number],
      default: [0, 0]
    },
    address: String
  },
  verified: {
    type: Boolean,
    default: false
  },
  verificationScore: {
    type: Number,
    default: 0,
    min: 0,
    max: 100
  },
  fcmToken: String,
  preferences: {
    notifications: {
      email: { type: Boolean, default: true },
      sms: { type: Boolean, default: false },
      push: { type: Boolean, default: true }
    },
    radius: {
      type: Number,
      default: 10
    }
  },
  lastActive: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

// Index for geospatial queries
userSchema.index({ location: '2dsphere' });

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();

  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Method to check password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
''',
        'backend/src/models/Incident.js': '''const mongoose = require('mongoose');

const incidentSchema = new mongoose.Schema({
  reporter: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  type: {
    type: String,
    enum: ['flood', 'fire', 'earthquake', 'storm', 'accident', 'medical', 'other'],
    required: true
  },
  severity: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    required: true
  },
  title: {
    type: String,
    required: true,
    trim: true,
    maxlength: 200
  },
  description: {
    type: String,
    required: true,
    maxlength: 2000
  },
  location: {
    type: {
      type: String,
      enum: ['Point'],
      required: true
    },
    coordinates: {
      type: [Number],
      required: true
    },
    address: String
  },
  images: [{
    url: String,
    caption: String
  }],
  status: {
    type: String,
    enum: ['pending', 'verified', 'in-progress', 'resolved', 'false-report'],
    default: 'pending'
  },
  verificationStatus: {
    verified: { type: Boolean, default: false },
    verifiedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    verifiedAt: Date,
    verificationNotes: String
  },
  affectedCount: {
    type: Number,
    default: 0
  },
  upvotes: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  responses: [{
    responder: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    action: String,
    timestamp: { type: Date, default: Date.now },
    notes: String
  }],
  metadata: {
    views: { type: Number, default: 0 },
    shares: { type: Number, default: 0 }
  }
}, {
  timestamps: true
});

// Geospatial index
incidentSchema.index({ location: '2dsphere' });

// Compound indexes for common queries
incidentSchema.index({ status: 1, createdAt: -1 });
incidentSchema.index({ type: 1, severity: 1 });

module.exports = mongoose.model('Incident', incidentSchema);
''',
        'backend/src/models/Resource.js': '''const mongoose = require('mongoose');

const resourceSchema = new mongoose.Schema({
  type: {
    type: String,
    enum: ['request', 'offer'],
    required: true
  },
  category: {
    type: String,
    enum: ['food', 'water', 'medical', 'shelter', 'clothing', 'transport', 'other'],
    required: true
  },
  itemName: {
    type: String,
    required: true,
    trim: true
  },
  quantity: {
    type: Number,
    required: true,
    min: 1
  },
  unit: {
    type: String,
    required: true
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  incident: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Incident'
  },
  location: {
    type: {
      type: String,
      enum: ['Point'],
      required: true
    },
    coordinates: {
      type: [Number],
      required: true
    },
    address: String
  },
  description: {
    type: String,
    maxlength: 500
  },
  urgency: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    default: 'medium'
  },
  status: {
    type: String,
    enum: ['available', 'matched', 'fulfilled', 'expired'],
    default: 'available'
  },
  matchedWith: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Resource'
  },
  expiresAt: Date,
  contactInfo: {
    phone: String,
    email: String,
    preferredContact: {
      type: String,
      enum: ['phone', 'email', 'app']
    }
  }
}, {
  timestamps: true
});

// Geospatial index
resourceSchema.index({ location: '2dsphere' });

// Compound indexes
resourceSchema.index({ type: 1, status: 1, category: 1 });

module.exports = mongoose.model('Resource', resourceSchema);
''',
        'backend/src/routes/authRoutes.js': '''const express = require('express');
const authController = require('../controllers/authController');
const { authMiddleware } = require('../middleware/authMiddleware');

const router = express.Router();

router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/logout', authMiddleware, authController.logout);
router.get('/me', authMiddleware, authController.getProfile);
router.put('/me', authMiddleware, authController.updateProfile);
router.post('/forgot-password', authController.forgotPassword);
router.post('/reset-password/:token', authController.resetPassword);

module.exports = router;
''',
        'backend/src/routes/incidentRoutes.js': '''const express = require('express');
const incidentController = require('../controllers/incidentController');
const { authMiddleware } = require('../middleware/authMiddleware');
const { uploadMiddleware } = require('../middleware/uploadMiddleware');

const router = express.Router();

router.get('/', incidentController.getIncidents);
router.get('/:id', incidentController.getIncidentById);
router.post('/', authMiddleware, uploadMiddleware.array('images', 5), incidentController.createIncident);
router.put('/:id', authMiddleware, incidentController.updateIncident);
router.delete('/:id', authMiddleware, incidentController.deleteIncident);
router.post('/:id/upvote', authMiddleware, incidentController.upvoteIncident);
router.post('/:id/verify', authMiddleware, incidentController.verifyIncident);
router.get('/nearby/:lat/:lng', incidentController.getNearbyIncidents);

module.exports = router;
''',
        'backend/src/middleware/authMiddleware.js': '''const jwt = require('jsonwebtoken');
const User = require('../models/User');

exports.authMiddleware = async (req, res, next) => {
  try {
    // Get token from header
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'No token provided. Authorization denied.'
      });
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Get user from token
    const user = await User.findById(decoded.id).select('-password');

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User not found. Authorization denied.'
      });
    }

    // Add user to request
    req.user = user;
    next();
  } catch (error) {
    console.error('Auth middleware error:', error);
    return res.status(401).json({
      success: false,
      message: 'Token is invalid or expired.'
    });
  }
};
''',
        'database/schema.sql': '''-- Users table
        CREATE TABLE IF NOT EXISTS users
        (
            id
            UUID
            PRIMARY
            KEY
            DEFAULT
            gen_random_uuid
        (
        ),
            name VARCHAR
        (
            255
        ) NOT NULL,
            email VARCHAR
        (
            255
        ) UNIQUE NOT NULL,
            password VARCHAR
        (
            255
        ) NOT NULL,
            phone VARCHAR
        (
            50
        ),
            role VARCHAR
        (
            50
        ) DEFAULT 'citizen',
            location GEOGRAPHY
        (
            POINT,
            4326
        ),
            verified BOOLEAN DEFAULT FALSE,
            verification_score INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

-- Incidents table
        CREATE TABLE IF NOT EXISTS incidents
        (
            id
            UUID
            PRIMARY
            KEY
            DEFAULT
            gen_random_uuid
        (
        ),
            reporter_id UUID REFERENCES users
        (
            id
        ),
            type VARCHAR
        (
            50
        ) NOT NULL,
            severity VARCHAR
        (
            50
        ) NOT NULL,
            title VARCHAR
        (
            200
        ) NOT NULL,
            description TEXT NOT NULL,
            location GEOGRAPHY
        (
            POINT,
            4326
        ) NOT NULL,
            address TEXT,
            status VARCHAR
        (
            50
        ) DEFAULT 'pending',
            verified BOOLEAN DEFAULT FALSE,
            affected_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

-- Resources table
        CREATE TABLE IF NOT EXISTS resources
        (
            id
            UUID
            PRIMARY
            KEY
            DEFAULT
            gen_random_uuid
        (
        ),
            user_id UUID REFERENCES users
        (
            id
        ),
            incident_id UUID REFERENCES incidents
        (
            id
        ),
            type VARCHAR
        (
            50
        ) NOT NULL,
            category VARCHAR
        (
            50
        ) NOT NULL,
            item_name VARCHAR
        (
            255
        ) NOT NULL,
            quantity INT NOT NULL,
            unit VARCHAR
        (
            50
        ) NOT NULL,
            location GEOGRAPHY
        (
            POINT,
            4326
        ) NOT NULL,
            urgency VARCHAR
        (
            50
        ) DEFAULT 'medium',
            status VARCHAR
        (
            50
        ) DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

-- Create spatial indexes
        CREATE INDEX idx_users_location ON users USING GIST(location);
        CREATE INDEX idx_incidents_location ON incidents USING GIST(location);
        CREATE INDEX idx_resources_location ON resources USING GIST(location);

-- Create compound indexes
        CREATE INDEX idx_incidents_status_created ON incidents (status, created_at DESC);
        CREATE INDEX idx_resources_type_status ON resources (type, status);
                               ''',
        'infrastructure/docker/docker-compose.yml': '''version: '3.8'

services:
  mongodb:
    image: mongo:6
    container_name: disaster_response_mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:7-alpine
    container_name: disaster_response_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ../../backend
      dockerfile: ../infrastructure/docker/Dockerfile.backend
    container_name: disaster_response_backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      NODE_ENV: production
      MONGODB_URI: mongodb://admin:password@mongodb:27017/disaster_response?authSource=admin
      REDIS_URL: redis://redis:6379
    depends_on:
      - mongodb
      - redis
    volumes:
      - ../../backend:/app
      - /app/node_modules

  frontend:
    build:
      context: ../../frontend
      dockerfile: ../infrastructure/docker/Dockerfile.frontend
    container_name: disaster_response_frontend
    restart: always
    ports:
      - "3000:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    container_name: disaster_response_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend

volumes:
  mongodb_data:
  redis_data:
''',
        'infrastructure/docker/Dockerfile.backend': '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

COPY . .

EXPOSE 5000

CMD ["npm", "start"]
''',
        'infrastructure/docker/Dockerfile.frontend': '''FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
'''
    }

    def create_structure(base_path, structure_dict):
        """Recursively create directories and files"""
        for key, value in structure_dict.items():
            if key == '__files__':
                for filename in value:
                    file_path = os.path.join(base_path, filename)

                    # Create file with template content if available
                    relative_path = os.path.relpath(file_path, project_root)
                    if relative_path in templates:
                        with open(file_path, 'w') as f:
                            f.write(templates[relative_path])
                        print(f'✓ Created file with template: {relative_path}')
                    else:
                        with open(file_path, 'w') as f:
                            f.write('')
                        print(f'✓ Created empty file: {relative_path}')
            elif isinstance(value, dict):
                dir_path = os.path.join(base_path, key)
                os.makedirs(dir_path, exist_ok=True)
                print(f'📁 Created directory: {os.path.relpath(dir_path, project_root)}')
                create_structure(dir_path, value)
            elif isinstance(value, list):
                dir_path = os.path.join(base_path, key)
                os.makedirs(dir_path, exist_ok=True)
                print(f'📁 Created directory: {os.path.relpath(dir_path, project_root)}')
                for filename in value:
                    file_path = os.path.join(dir_path, filename)
                    with open(file_path, 'w') as f:
                        f.write('')
                    print(f'  ✓ Created file: {filename}')

    # Project structure definition
    structure = {
        'frontend': {
            'public': ['index.html', 'manifest.json', 'service-worker.js'],
            'src': {
                'assets': {
                    'images': [],
                    'icons': [],
                    'styles': []
                },
                'components': {
                    'common': ['Header.jsx', 'Footer.jsx', 'Loader.jsx', 'Modal.jsx', 'Alert.jsx'],
                    'map': ['MapView.jsx', 'IncidentMarker.jsx', 'HeatmapLayer.jsx', 'LocationPicker.jsx'],
                    'incident': ['IncidentForm.jsx', 'IncidentCard.jsx', 'IncidentDetails.jsx', 'IncidentList.jsx',
                                 'VerificationPanel.jsx'],
                    'resource': ['ResourceRequest.jsx', 'ResourceOffer.jsx', 'ResourceMatch.jsx',
                                 'ResourceInventory.jsx'],
                    'volunteer': ['VolunteerSignup.jsx', 'VolunteerDashboard.jsx', 'TaskAssignment.jsx'],
                    'communication': ['Chat.jsx', 'MessageThread.jsx', 'EmergencyAlert.jsx']
                },
                'pages': ['Home.jsx', 'Dashboard.jsx', 'Login.jsx', 'Register.jsx', 'ReportIncident.jsx',
                          'IncidentMap.jsx', 'Resources.jsx', 'Profile.jsx', 'AdminPanel.jsx'],
                'services': ['api.js', 'authService.js', 'incidentService.js', 'resourceService.js',
                             'volunteerService.js', 'notificationService.js', 'geolocationService.js'],
                'store': {
                    'slices': ['authSlice.js', 'incidentSlice.js', 'resourceSlice.js', 'notificationSlice.js'],
                    'middleware': [],
                    '__files__': ['index.js']
                },
                'hooks': ['useAuth.js', 'useGeolocation.js', 'useWebSocket.js', 'useOfflineSync.js'],
                'utils': ['validation.js', 'formatters.js', 'constants.js', 'helpers.js'],
                '__files__': ['App.jsx', 'index.js', 'routes.js']
            },
            '__files__': ['package.json', '.env']
        },
        'backend': {
            'src': {
                'config': ['database.js', 'redis.js', 's3.js', 'firebase.js', 'env.js'],
                'models': ['User.js', 'Incident.js', 'Resource.js', 'Volunteer.js', 'Message.js',
                           'Notification.js', 'VerificationLog.js'],
                'controllers': ['authController.js', 'incidentController.js', 'resourceController.js',
                                'volunteerController.js', 'messageController.js', 'notificationController.js',
                                'analyticsController.js'],
                'routes': ['authRoutes.js', 'incidentRoutes.js', 'resourceRoutes.js', 'volunteerRoutes.js',
                           'messageRoutes.js', 'adminRoutes.js'],
                'middleware': ['authMiddleware.js', 'roleMiddleware.js', 'validationMiddleware.js',
                               'rateLimiter.js', 'errorHandler.js', 'uploadMiddleware.js'],
                'services': ['emailService.js', 'smsService.js', 'pushNotificationService.js',
                             'geocodingService.js', 'imageProcessing.js', 'mlVerification.js',
                             'matchingAlgorithm.js'],
                'websocket': ['socketHandler.js', 'rooms.js', 'events.js'],
                'utils': ['logger.js', 'validators.js', 'helpers.js', 'constants.js'],
                'jobs': ['incidentAggregation.js', 'notificationScheduler.js', 'dataCleanup.js'],
                '__files__': ['app.js', 'server.js']
            },
            'tests': {
                'unit': [],
                'integration': [],
                'e2e': []
            },
            '__files__': ['package.json', '.env', 'ecosystem.config.js']
        },
        'mobile': {
            'android': [],
            'ios': [],
            'src': {
                'components': [],
                'screens': ['HomeScreen.js', 'MapScreen.js', 'ReportScreen.js', 'ChatScreen.js', 'ProfileScreen.js'],
                'navigation': ['AppNavigator.js'],
                'services': [],
                'store': [],
                'utils': [],
                '__files__': ['App.js']
            },
            '__files__': ['package.json', 'app.json']
        },
        'admin-dashboard': {
            'src': {
                'components': {
                    'analytics': ['IncidentAnalytics.jsx', 'ResourceMetrics.jsx', 'ResponseTime.jsx'],
                    'moderation': ['ReportQueue.jsx', 'UserManagement.jsx', 'ContentModeration.jsx'],
                    'settings': ['SystemConfig.jsx', 'AlertRules.jsx']
                },
                'pages': ['Overview.jsx', 'IncidentManagement.jsx', 'UserManagement.jsx', 'Reports.jsx']
            },
            '__files__': ['package.json']
        },
        'shared': {
            'types': ['incident.types.ts', 'user.types.ts', 'resource.types.ts'],
            'constants': ['roles.js', 'statuses.js', 'categories.js']
        },
        'database': {
            'migrations': [],
            'seeds': [],
            '__files__': ['schema.sql']
        },
        'infrastructure': {
            'docker': ['Dockerfile.backend', 'Dockerfile.frontend', 'docker-compose.yml'],
            'kubernetes': {
                'deployments': [],
                'services': [],
                'configmaps': []
            },
            'nginx': ['nginx.conf'],
            'scripts': ['deploy.sh', 'backup.sh']
        },
        'docs': ['API.md', 'ARCHITECTURE.md', 'DEPLOYMENT.md', 'USER_GUIDE.md'],
        '.github': {
            'workflows': ['ci.yml', 'cd.yml']
        },
        '__files__': ['.gitignore', 'README.md', 'package.json']
    }

    # Get current directory
    project_root = os.path.join(os.getcwd(), 'disaster-response-system')

    # Create root directory
    os.makedirs(project_root, exist_ok=True)
    print(f'\n{"=" * 70}')
    print(f'🚀 Creating Disaster Response System')
    print(f'📍 Location: {project_root}')
    print(f'{"=" * 70}\n')

    # Create package.json files first
    print('📦 Creating package.json files...\n')

    with open(os.path.join(project_root, 'package.json'), 'w') as f:
        json.dump(root_package, f, indent=2)
    print('✓ Created root package.json')

    os.makedirs(os.path.join(project_root, 'frontend'), exist_ok=True)
    with open(os.path.join(project_root, 'frontend', 'package.json'), 'w') as f:
        json.dump(frontend_package, f, indent=2)
    print('✓ Created frontend/package.json')

    os.makedirs(os.path.join(project_root, 'backend'), exist_ok=True)
    with open(os.path.join(project_root, 'backend', 'package.json'), 'w') as f:
        json.dump(backend_package, f, indent=2)
    print('✓ Created backend/package.json')

    os.makedirs(os.path.join(project_root, 'mobile'), exist_ok=True)
    with open(os.path.join(project_root, 'mobile', 'package.json'), 'w') as f:
        json.dump(mobile_package, f, indent=2)
    print('✓ Created mobile/package.json')

    os.makedirs(os.path.join(project_root, 'admin-dashboard'), exist_ok=True)
    with open(os.path.join(project_root, 'admin-dashboard', 'package.json'), 'w') as f:
        json.dump(admin_package, f, indent=2)
    print('✓ Created admin-dashboard/package.json')

    print('\n📁 Creating directory structure...\n')

    # Create the entire structure
    create_structure(project_root, structure)

    print(f'\n{"=" * 70}')
    print('✅ Project structure created successfully!')
    print(f'{"=" * 70}\n')

    print('📋 Next Steps:\n')
    print('1. Open the project in PyCharm:')
    print(f'   File → Open → {project_root}\n')
    print('2. Install dependencies:')
    print('   cd disaster-response-system')
    print('   npm run install:all\n')
    print('3. Configure environment variables:')
    print('   - Edit backend/.env with your configuration')
    print('   - Edit frontend/.env with your API URL\n')
    print('4. Start MongoDB and Redis (using Docker):')
    print('   cd infrastructure/docker')
    print('   docker-compose up mongodb redis\n')
    print('5. Start development servers:')
    print('   npm run dev:backend   # Terminal 1')
    print('   npm run dev:frontend  # Terminal 2\n')
    print('📚 Check the README.md for detailed documentation!\n')


if __name__ == '__main__':
    try:
        create_project_structure()
    except Exception as e:
        print(f'\n❌ Error: {str(e)}')
        print('Make sure you have write permissions in the current directory.')