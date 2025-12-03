import os
import subprocess
import sys


def force_fix():
    base_path = os.getcwd()
    frontend_path = os.path.join(base_path, 'frontend')
    root_pkg = os.path.join(base_path, 'package.json')
    root_pkg_backup = os.path.join(base_path, 'package.json.bak')

    print("🔧 STARTING FORCE FIX...\n")

    # STEP 1: Disable Root package.json temporarily
    # This stops npm from trying to be smart about "workspaces"
    if os.path.exists(root_pkg):
        print(f"📦 Found root package.json. Renaming to package.json.bak to avoid conflicts...")
        try:
            if os.path.exists(root_pkg_backup):
                os.remove(root_pkg_backup)
            os.rename(root_pkg, root_pkg_backup)
            print("   ✓ Root package.json disabled.")
        except Exception as e:
            print(f"   ⚠️ Could not rename root package.json: {e}")

    # STEP 2: Force install react-scripts
    print("\n📦 Force installing 'react-scripts' directly...")
    print("   Running: npm install react-scripts --save")

    try:
        # We explicitly install react-scripts to ensure the binary exists
        subprocess.check_call("npm install react-scripts --save", shell=True, cwd=frontend_path)

        # We also run a full install to get everything else
        print("\n📦 Ensuring all other dependencies are installed...")
        subprocess.check_call("npm install", shell=True, cwd=frontend_path)
        print("\n✅ Dependencies installed successfully!")

    except subprocess.CalledProcessError:
        print("\n❌ Install failed. Please check your internet connection.")
        # Restore the file before exiting
        if os.path.exists(root_pkg_backup):
            os.rename(root_pkg_backup, root_pkg)
        return

    # STEP 3: Start the server
    print("\n🚀 Starting the Frontend Server...")
    print("   Running: npm start")

    try:
        subprocess.check_call("npm start", shell=True, cwd=frontend_path)
    except subprocess.CalledProcessError:
        print("\n❌ Server stopped.")
    finally:
        # STEP 4: Restore Root package.json (Optional, but good practice)
        if os.path.exists(root_pkg_backup):
            print("\n🔄 Restoring root package.json...")
            os.rename(root_pkg_backup, root_pkg)


if __name__ == "__main__":
    force_fix()