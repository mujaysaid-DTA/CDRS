import os
import shutil
import subprocess


def deep_clean():
    base_path = os.getcwd()

    # Locations to clean
    targets = [
        # The Root (Should not have node_modules usually)
        os.path.join(base_path, 'node_modules'),
        os.path.join(base_path, 'package-lock.json'),

        # The Frontend (The one we actually need)
        os.path.join(base_path, 'frontend', 'node_modules'),
        os.path.join(base_path, 'frontend', 'package-lock.json'),
    ]

    print("🧹 STARTING DEEP CLEAN...")
    print("   (This will fix the path confusion)\n")

    for target in targets:
        if os.path.exists(target):
            print(f"   Deleting: {target}")
            try:
                if os.path.isfile(target):
                    os.remove(target)
                else:
                    shutil.rmtree(target)  # Deletes folders
                print("   ✅ Deleted.")
            except Exception as e:
                print(f"   ⚠️ Could not delete {target}: {e}")
        else:
            print(f"   (Clean) {os.path.basename(target)} not found.")

    # Clear NPM Cache (Crucial for "Missing Module" errors)
    print("\n🚿 Cleaning NPM Cache...")
    try:
        subprocess.run("npm cache clean --force", shell=True)
        print("   ✅ Cache Cleared.")
    except:
        print("   ⚠️ Could not clear cache (not critical).")

    print("\n" + "=" * 50)
    print("✨ SYSTEM IS CLEAN ✨")
    print("=" * 50)
    print("Now, perform the Fresh Install manually to watch the progress:")
    print("1. cd frontend")
    print("2. npm install")
    print("3. npm start")


if __name__ == "__main__":
    deep_clean()