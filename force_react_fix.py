import os
import json
import subprocess


def force_fix():
    base_path = os.getcwd()
    frontend_path = os.path.join(base_path, 'frontend')
    package_json_path = os.path.join(frontend_path, 'package.json')

    print("🚑 STARTING EMERGENCY REACT FIX\n")

    # 1. Force-Write the correct package.json
    # This ensures 'react-scripts' is definitely listed as a dependency
    print("1. Overwriting package.json with correct dependencies...")

    package_content = {
        "name": "disaster-response-frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "@testing-library/jest-dom": "^5.17.0",
            "@testing-library/react": "^13.4.0",
            "@testing-library/user-event": "^13.5.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-icons": "^4.10.1",
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

    try:
        with open(package_json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(package_content, indent=2))
        print("   ✅ package.json fixed.")
    except Exception as e:
        print(f"   ❌ Failed to write file: {e}")
        return

    # 2. Force Install specifically for react-scripts
    print("\n2. Force installing react-scripts (The missing engine)...")
    print("   (This takes 30-60 seconds. Please wait.)")

    try:
        # We run this explicitly to ensure the binary is linked
        subprocess.check_call("npm install", shell=True, cwd=frontend_path)
        print("   ✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("   ❌ npm install failed.")
        return

    # 3. Start the server
    print("\n3. Launching Application...")
    print("   Running: npm start")
    try:
        subprocess.check_call("npm start", shell=True, cwd=frontend_path)
    except subprocess.CalledProcessError:
        print("\n❌ Server crashed.")


if __name__ == "__main__":
    force_fix()