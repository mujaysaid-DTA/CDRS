import os
import json


def fix_setup():
    # Get the current working directory
    base_path = os.getcwd()
    frontend_path = os.path.join(base_path, 'frontend')
    backend_path = os.path.join(base_path, 'backend')

    print("🔧 Diagnosing Project Setup...\n")

    # --- 1. Fix Backend package.json ---
    # We check if backend config exists, if not we create it
    backend_pkg_path = os.path.join(backend_path, 'package.json')
    if not os.path.exists(backend_pkg_path):
        print("⚠️ Backend package.json missing. Creating it...")
        backend_package = {
            "name": "disaster-response-api",
            "version": "1.0.0",
            "main": "src/server.js",
            "scripts": {
                "start": "node src/server.js",
                "dev": "nodemon src/server.js"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "dotenv": "^16.3.1",
                "body-parser": "^1.20.2",
                "uuid": "^9.0.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.1"
            }
        }
        with open(backend_pkg_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(backend_package, indent=2))
        print("✅ Created backend/package.json")
    else:
        print("✅ Backend package.json exists.")

    # --- 2. Fix Frontend package.json ---
    # This is likely the missing piece causing your 'missing script' error
    frontend_pkg_path = os.path.join(frontend_path, 'package.json')

    if not os.path.exists(frontend_pkg_path):
        print("❌ Frontend package.json is MISSING. Fixing it now...")

        frontend_package = {
            "name": "disaster-response-frontend",
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "@testing-library/jest-dom": "^5.17.0",
                "@testing-library/react": "^13.4.0",
                "@testing-library/user-event": "^13.5.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.16.0",
                "react-scripts": "5.0.1",
                "web-vitals": "^2.1.4"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": [
                    "react-app",
                    "react-app/jest"
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
            }
        }

        with open(frontend_pkg_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(frontend_package, indent=2))
        print("✅ Created frontend/package.json")
    else:
        print("✅ Frontend package.json exists.")

    print("\n" + "=" * 50)
    print("🎉 FIX COMPLETE")
    print("=" * 50)
    print("NOW YOU MUST RUN 'npm install' IN BOTH FOLDERS.")


if __name__ == "__main__":
    fix_setup()