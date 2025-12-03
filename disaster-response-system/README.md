# Disaster Response System

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
