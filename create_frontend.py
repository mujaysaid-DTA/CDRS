import os


def create_frontend_files():
    """
    Creates basic React files to get the frontend working
    """

    # Assuming we're in the disaster-response-system directory
    frontend_path = os.path.join(os.getcwd(), 'frontend', 'src')
    public_path = os.path.join(os.getcwd(), 'frontend', 'public')

    print("Creating frontend starter files...\n")

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Disaster Response System - Crowdsourcing platform for emergency response" />
    <title>Disaster Response System</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''

    # src/index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

    # src/index.css
    index_css = '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
'''

    # src/App.jsx
    app_jsx = '''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="hero-section">
          <h1>🚨 Disaster Response System</h1>
          <p className="subtitle">Crowdsourcing Emergency Response & Resource Coordination</p>

          <div className="features-grid">
            <div className="feature-card">
              <div className="icon">📍</div>
              <h3>Report Incidents</h3>
              <p>Real-time disaster reporting with geolocation</p>
            </div>

            <div className="feature-card">
              <div className="icon">🗺️</div>
              <h3>Interactive Map</h3>
              <p>View incidents and resources on live map</p>
            </div>

            <div className="feature-card">
              <div className="icon">🤝</div>
              <h3>Resource Matching</h3>
              <p>Connect those in need with available help</p>
            </div>

            <div className="feature-card">
              <div className="icon">👥</div>
              <h3>Volunteer Network</h3>
              <p>Coordinate response efforts efficiently</p>
            </div>
          </div>

          <div className="cta-buttons">
            <button className="btn btn-primary">Report Emergency</button>
            <button className="btn btn-secondary">View Map</button>
          </div>

          <div className="status-bar">
            <div className="status-item">
              <span className="status-label">Backend:</span>
              <span className="status-value" id="backend-status">Checking...</span>
            </div>
            <div className="status-item">
              <span className="status-label">Database:</span>
              <span className="status-value" id="db-status">Checking...</span>
            </div>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
'''

    # src/App.css
    app_css = '''.App {
  text-align: center;
  min-height: 100vh;
}

.App-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
  padding: 20px;
}

.hero-section {
  max-width: 1200px;
  width: 100%;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: fadeInDown 1s ease-out;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  opacity: 0.9;
  animation: fadeInUp 1s ease-out;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
  animation: fadeIn 1.5s ease-out;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.feature-card .icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  font-size: 0.9rem;
  opacity: 0.8;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 3rem 0;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-primary {
  background: #ff6b6b;
  color: white;
}

.btn-primary:hover {
  background: #ee5a52;
  transform: scale(1.05);
  box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
  transform: scale(1.05);
}

.status-bar {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-top: 3rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  font-size: 0.9rem;
}

.status-item {
  display: flex;
  gap: 0.5rem;
}

.status-label {
  font-weight: 600;
}

.status-value {
  color: #4ade80;
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .status-bar {
    flex-direction: column;
    gap: 0.5rem;
  }
}
'''

    # Write files
    files = [
        (os.path.join(public_path, 'index.html'), index_html),
        (os.path.join(frontend_path, 'index.js'), index_js),
        (os.path.join(frontend_path, 'index.css'), index_css),
        (os.path.join(frontend_path, 'App.jsx'), app_jsx),
        (os.path.join(frontend_path, 'App.css'), app_css)
    ]

    for file_path, content in files:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"✗ Error creating {os.path.basename(file_path)}: {str(e)}")

    print("\n" + "=" * 70)
    print("✅ Frontend starter files created!")
    print("=" * 70)
    print("\nThe React app should auto-reload in your browser.")
    print("If not, press Ctrl+C in the frontend terminal and run: npm start")
    print("\nYou should now see a beautiful landing page! 🎉")


if __name__ == '__main__':
    try:
        create_frontend_files()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you're running this from: C:\\project\\disaster-response-system")