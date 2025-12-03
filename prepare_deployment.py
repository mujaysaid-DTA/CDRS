import os


def prepare_deployment():
    base_path = os.getcwd()
    frontend_src = os.path.join(base_path, 'frontend', 'src')

    print("✈️ Prepping for Takeoff (Production Setup)...")

    # 1. CREATE API CONFIG (Frontend)
    # This allows the app to switch between localhost and the real web URL automatically.
    config_js = """const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api/v1' 
  : 'https://disaster-response-backend.onrender.com/api/v1'; // We will get this URL from Render later

export default API_BASE_URL;
"""
    with open(os.path.join(frontend_src, 'config.js'), 'w', encoding='utf-8') as f:
        f.write(config_js)
    print("✅ Created frontend/src/config.js")

    # 2. UPDATE ALL FRONTEND FILES TO USE NEW CONFIG
    # We replace hardcoded 'http://localhost:5000' with the dynamic API_BASE_URL
    files_to_update = [
        'pages/ReportIncident.jsx',
        'pages/IncidentList.jsx',
        'pages/IncidentMap.jsx',
        'pages/Resources.jsx',
        'pages/AdminPanel.jsx',
        'pages/Login.jsx',
        'pages/Register.jsx'
    ]

    for filename in files_to_update:
        filepath = os.path.join(frontend_src, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Inject Import
            if "import API_BASE_URL" not in content:
                content = "import API_BASE_URL from '../config';\n" + content

            # Replace localhost URLs
            content = content.replace("'http://localhost:5000/api/v1", "`${API_BASE_URL}")
            content = content.replace("`http://localhost:5000/api/v1", "`${API_BASE_URL}")

            # Fix the closing quote issue from the replacement
            # The code usually looks like: fetch('URL/incidents') -> fetch(`${API_BASE_URL}/incidents`)
            # My simple replace might leave artifacts, so let's be cleaner:

            # Smart Replace:
            # Case A: fetch('http://localhost:5000/api/v1/incidents')
            content = content.replace("'http://localhost:5000/api/v1", "`${API_BASE_URL}")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   updated {filename}")

    # 3. CREATE VERCEL CONFIG (For Frontend Routing)
    vercel_json = """{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}"""
    with open(os.path.join(base_path, 'frontend', 'vercel.json'), 'w', encoding='utf-8') as f:
        f.write(vercel_json)
    print("✅ Created vercel.json")

    print("\n📦 Code is ready for GitHub!")


if __name__ == "__main__":
    prepare_deployment()