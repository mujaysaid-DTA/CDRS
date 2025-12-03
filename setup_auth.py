import os
import json


def setup_auth():
    base_path = os.getcwd()
    backend_src = os.path.join(base_path, 'backend', 'src')
    frontend_src = os.path.join(base_path, 'frontend', 'src')
    data_path = os.path.join(base_path, 'backend', 'data', 'users.json')

    print("🔐 Building Authentication System (Login/Register)...\n")

    # --- PART 1: BACKEND (The Security Layer) ---

    # 1. Create Users Data File
    if not os.path.exists(data_path):
        # Create one default admin user
        default_users = [
            {
                "id": "admin-001",
                "name": "System Administrator",
                "email": "admin@drs.com",
                "password": "admin",  # In real app, this would be hashed
                "role": "admin",
                "createdAt": "2023-01-01T00:00:00.000Z"
            }
        ]
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, 'w') as f:
            json.dump(default_users, f, indent=2)

    # 2. authController.js
    auth_controller = '''const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/users.json');

const readUsers = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE));
};

const writeUsers = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

// @desc    Register a new user
// @route   POST /api/v1/auth/register
exports.register = (req, res) => {
  const { name, email, password, role } = req.body;
  const users = readUsers();

  if (users.find(u => u.email === email)) {
    return res.status(400).json({ message: 'User already exists' });
  }

  const newUser = {
    id: uuidv4(),
    name,
    email,
    password, // Note: We should hash this in production!
    role: role || 'user', // 'user', 'volunteer', 'admin'
    createdAt: new Date().toISOString()
  };

  users.push(newUser);
  writeUsers(users);

  res.status(201).json({
    id: newUser.id,
    name: newUser.name,
    email: newUser.email,
    role: newUser.role,
    token: 'mock-jwt-token-' + newUser.id // Mock token for now
  });
};

// @desc    Login user
// @route   POST /api/v1/auth/login
exports.login = (req, res) => {
  const { email, password } = req.body;
  const users = readUsers();

  const user = users.find(u => u.email === email && u.password === password);

  if (user) {
    res.json({
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      token: 'mock-jwt-token-' + user.id
    });
  } else {
    res.status(401).json({ message: 'Invalid email or password' });
  }
};
'''

    # 3. authRoutes.js
    auth_routes = '''const express = require('express');
const router = express.Router();
const { register, login } = require('../controllers/authController');

router.post('/register', register);
router.post('/login', login);

module.exports = router;
'''

    # 4. Inject into app.js
    app_js_path = os.path.join(backend_src, 'app.js')
    with open(app_js_path, 'r', encoding='utf-8') as f:
        app_content = f.read()

    if "authRoutes" not in app_content:
        app_content = app_content.replace(
            "const resourceRoutes = require('./routes/resourceRoutes');",
            "const resourceRoutes = require('./routes/resourceRoutes');\nconst authRoutes = require('./routes/authRoutes');"
        )
        app_content = app_content.replace(
            "app.use('/api/v1/resources', resourceRoutes);",
            "app.use('/api/v1/resources', resourceRoutes);\napp.use('/api/v1/auth', authRoutes);"
        )
        with open(app_js_path, 'w', encoding='utf-8') as f:
            f.write(app_content)
            print("✅ Backend Configured (Auth Routes Added)")

    # Write Backend Files
    with open(os.path.join(backend_src, 'controllers', 'authController.js'), 'w') as f:
        f.write(auth_controller)
    with open(os.path.join(backend_src, 'routes', 'authRoutes.js'), 'w') as f:
        f.write(auth_routes)

    # --- PART 2: FRONTEND (The UI Layer) ---

    # 5. Login.jsx
    login_page = '''import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Auth.css';

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await res.json();

      if (res.ok) {
        // Save user to local storage (basic session)
        localStorage.setItem('user', JSON.stringify(data));

        // Redirect based on role
        if (data.role === 'admin') navigate('/admin');
        else navigate('/resources');
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('Server error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>👋 Welcome Back</h2>
        <p>Sign in to continue coordination</p>

        {error && <div className="error-msg">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input 
              type="email" 
              required 
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              required 
              value={formData.password}
              onChange={e => setFormData({...formData, password: e.target.value})}
            />
          </div>
          <button type="submit" className="auth-btn">Sign In</button>
        </form>

        <p className="auth-link">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
'''

    # 6. Register.jsx
    register_page = '''import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Auth.css';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ name: '', email: '', password: '', role: 'volunteer' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://localhost:5000/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('user', JSON.stringify(data));
        navigate('/resources');
      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError('Server error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>🚀 Join the Force</h2>
        <p>Create an account to help your community</p>

        {error && <div className="error-msg">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input 
              type="text" 
              required 
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input 
              type="email" 
              required 
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              required 
              value={formData.password}
              onChange={e => setFormData({...formData, password: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>I want to...</label>
            <select 
              value={formData.role} 
              onChange={e => setFormData({...formData, role: e.target.value})}
            >
              <option value="volunteer">Volunteer (Offer Help)</option>
              <option value="user">Report Incidents (Seek Help)</option>
            </select>
          </div>
          <button type="submit" className="auth-btn">Create Account</button>
        </form>

        <p className="auth-link">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
'''

    # 7. Auth.css
    auth_css = '''.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
}

.auth-box {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.auth-box h2 { text-align: center; color: #1f2937; margin-bottom: 0.5rem; }
.auth-box p { text-align: center; color: #6b7280; margin-bottom: 2rem; }

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; color: #374151; }

.auth-box input, .auth-box select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.auth-btn {
  width: 100%;
  padding: 0.9rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.2s;
}

.auth-btn:hover { background: #2563eb; }

.auth-link { margin-top: 1.5rem; font-size: 0.9rem; }
.auth-link a { color: #3b82f6; text-decoration: none; font-weight: 600; }

.error-msg {
  background: #fee2e2;
  color: #dc2626;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  text-align: center;
}
'''

    with open(os.path.join(frontend_src, 'pages', 'Login.jsx'), 'w', encoding='utf-8') as f:
        f.write(login_page)
    with open(os.path.join(frontend_src, 'pages', 'Register.jsx'), 'w', encoding='utf-8') as f:
        f.write(register_page)
    with open(os.path.join(frontend_src, 'pages', 'Auth.css'), 'w', encoding='utf-8') as f:
        f.write(auth_css)

    # 8. Update App.jsx to include Login/Register Routes and a "Login" button
    app_jsx_path = os.path.join(frontend_src, 'App.jsx')
    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "Login" not in content:
        content = content.replace(
            "import AdminPanel from './pages/AdminPanel';",
            "import AdminPanel from './pages/AdminPanel';\nimport Login from './pages/Login';\nimport Register from './pages/Register';"
        )
        content = content.replace(
            '<Route path="/admin" element={<AdminPanel />} />',
            '<Route path="/admin" element={<AdminPanel />} />\n        <Route path="/login" element={<Login />} />\n        <Route path="/register" element={<Register />} />'
        )
        # Add Login button to Hero Section
        content = content.replace(
            '<Link to="/resources" className="cta-button secondary" style={{background: \'#f59e0b\', borderColor: \'#f59e0b\'}}>Resources</Link>',
            '<Link to="/resources" className="cta-button secondary" style={{background: \'#f59e0b\', borderColor: \'#f59e0b\'}}>Resources</Link>\n            <Link to="/login" className="cta-button secondary" style={{background: \'#1f2937\', borderColor: \'#1f2937\'}}>Login</Link>'
        )

        with open(app_jsx_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ App.jsx updated with Auth Routes")

    print("\n🚀 Authentication System Ready!")
    print("Default Admin Login:")
    print("  Email: admin@drs.com")
    print("  Pass:  admin")


if __name__ == "__main__":
    setup_auth()