import os
import shutil
import subprocess
import sys


def repair_frontend():
    base_path = os.getcwd()
    frontend_path = os.path.join(base_path, 'frontend')
    node_modules_path = os.path.join(frontend_path, 'node_modules')
    package_lock_path = os.path.join(frontend_path, 'package-lock.json')

    print(f"🔧 Starting Repair on: {frontend_path}\n")

    # 1. Check if frontend folder exists
    if not os.path.exists(frontend_path):
        print("❌ Error: 'frontend' folder not found.")
        return

    # 2. Clean up existing install (The "Nuclear Option")
    if os.path.exists(node_modules_path):
        print("🗑️  Deleting corrupted node_modules (this takes a moment)...")
        try:
            shutil.rmtree(node_modules_path)  # Wipes the folder
            print("   ✓ Deleted node_modules")
        except Exception as e:
            print(f"   ⚠️ Could not fully delete node_modules: {e}")

    if os.path.exists(package_lock_path):
        try:
            os.remove(package_lock_path)
            print("   ✓ Deleted package-lock.json")
        except:
            pass

    # 3. Verify package.json exists
    if not os.path.exists(os.path.join(frontend_path, 'package.json')):
        print("❌ Error: package.json is missing! Run 'fix_project_setup.py' first.")
        return

    # 4. Run npm install
    print("\n📦 Installing dependencies (this may take 1-2 minutes)...")
    print("   Running: npm install")

    # We use shell=True to ensure it finds the npm command
    try:
        subprocess.check_call("npm install", shell=True, cwd=frontend_path)
        print("\n✅ Installation Successful!")
    except subprocess.CalledProcessError:
        print("\n❌ 'npm install' Failed.")
        print("   Please check your internet connection or Node.js version.")
        return

    # 5. Start the server
    print("\n🚀 Attempting to start the server...")
    print("   Running: npm start")
    try:
        subprocess.check_call("npm start", shell=True, cwd=frontend_path)
    except subprocess.CalledProcessError:
        print("\n❌ Server crashed.")


if __name__ == "__main__":
    repair_frontend()