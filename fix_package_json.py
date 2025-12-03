import os
import json

def fix_package_json_files():
    """
    Fixes the package.json files with proper content
    """
    
    # Get the project root (assumes script is run from project folder)
    project_root = os.getcwd()
    
    print(f"Fixing package.json files in: {project_root}\n")
    
    # Root package.json
    root_package = {
        "name": "disaster-response-system",
        "version": "1.0.0",
        "private": True,
        "workspaces": [
            "frontend",
            "backend",
            "mobile",
            "admin-dashboard"
        ],
        "scripts": {
            "install:all": "cd frontend && npm install && cd ../backend && npm install && cd ../mobile && npm install && cd ../admin-dashboard && npm install",
            "dev:frontend": "cd frontend && npm start",
            "dev:backend": "cd backend && npm run dev",
            "dev:admin": "cd admin-dashboard && npm start",
            "build:all": "cd frontend && npm run build && cd ../admin-dashboard && npm run build"
        },
        "devDependencies": {}
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
        "eslintConfig": {
            "extends": [
                "react-app"
            ]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
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
        },
        "devDependencies": {
            "@babel/core": "^7.20.0"
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
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "eslintConfig": {
            "extends": [
                "react-app"
            ]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        },
        "devDependencies": {
            "react-scripts": "5.0.1"
        }
    }
    
    # Write all package.json files
    files_to_create = [
        ('package.json', root_package),
        (os.path.join('frontend', 'package.json'), frontend_package),
        (os.path.join('backend', 'package.json'), backend_package),
        (os.path.join('mobile', 'package.json'), mobile_package),
        (os.path.join('admin-dashboard', 'package.json'), admin_package)
    ]
    
    for file_path, content in files_to_create:
        full_path = os.path.join(project_root, file_path)
        
        try:
            with open(full_path, 'w') as f:
                json.dump(content, f, indent=2)
            print(f"✓ Fixed: {file_path}")
        except Exception as e:
            print(f"✗ Error fixing {file_path}: {str(e)}")
    
    print("\n" + "="*70)
    print("✅ All package.json files have been fixed!")
    print("="*70)
    print("\nNow you can run:")
    print("  npm run install:all")
    print("\nOr install each one separately:")
    print("  cd frontend && npm install")
    print("  cd backend && npm install")
    print("  cd mobile && npm install")
    print("  cd admin-dashboard && npm install")

if __name__ == '__main__':
    try:
        fix_package_json_files()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you're running this script from inside the disaster-response-system folder!")
        print("Example: cd C:\\project\\disaster-response-system")
        print("         python fix_package_json.py")