import os
import subprocess
import platform


def kill_port_5000():
    print("🔫 Hunting down process on Port 5000...")

    system = platform.system()

    if system == "Windows":
        try:
            # Find the PID (Process ID)
            output = subprocess.check_output("netstat -ano | findstr :5000", shell=True).decode()
            lines = output.strip().split('\n')

            pids_killed = set()

            for line in lines:
                parts = line.strip().split()
                # The PID is usually the last item
                pid = parts[-1]

                if pid and pid != "0" and pid not in pids_killed:
                    print(f"   Found Zombie Process (PID: {pid})")
                    # Kill it
                    os.system(f"taskkill /F /PID {pid}")
                    pids_killed.add(pid)
                    print("   💥 Terminated.")

            if not pids_killed:
                print("   No process found on port 5000.")

        except subprocess.CalledProcessError:
            print("   No process found on port 5000.")
    else:
        # Linux/Mac
        os.system("lsof -ti:5000 | xargs kill -9")

    print("\n✅ Port 5000 is now free.")


if __name__ == "__main__":
    kill_port_5000()