import os


def connect_backend():
    base_path = os.getcwd()
    config_path = os.path.join(base_path, 'frontend', 'src', 'config.js')

    # YOUR RENDER URL
    backend_url = "https://disaster-response-system.onrender.com"

    print(f"🔗 Connecting Frontend to: {backend_url} ...")

    js_content = f"""const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api/v1' 
  : '{backend_url}/api/v1';

export default API_BASE_URL;
"""

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print("✅ Configuration updated! Your app now knows where the server is.")


if __name__ == "__main__":
    connect_backend()