import os


def unify_theme():
    base_path = os.getcwd()
    pages_path = os.path.join(base_path, 'frontend', 'src', 'pages')

    print("🎨 Unifying App Theme (Applying Dark Mode Everywhere)...")

    # 1. AUTH CSS (Login/Register)
    auth_css = """.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Use the global dark background */
  background: transparent; 
}

.auth-box {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2.5rem;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
  color: white;
}

.auth-box h2 { text-align: center; color: white; margin-bottom: 0.5rem; }
.auth-box p { text-align: center; color: #94a3b8; margin-bottom: 2rem; }

.form-group label { color: #cbd5e1; }

.auth-box input, .auth-box select {
  width: 100%;
  padding: 0.8rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 1rem;
  color: white;
  margin-bottom: 1rem;
}

.auth-box input:focus {
  outline: none;
  border-color: #6366f1; /* Primary color */
}

.auth-btn {
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  border: none;
  padding: 0.9rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  transition: transform 0.2s;
}

.auth-btn:hover { transform: scale(1.02); }

.auth-link a { color: #818cf8; }
"""

    # 2. RESOURCES CSS (Volunteer Hub)
    resources_css = """.resources-page {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  color: white;
}

.res-header { text-align: center; margin-bottom: 2rem; }
.res-header h1 { color: white; }

.tab {
  background: rgba(255,255,255,0.1);
  color: #cbd5e1;
  border: 1px solid rgba(255,255,255,0.1);
}
.tab:hover { background: rgba(255,255,255,0.2); }

/* Active Tabs */
.tab.active.req { background: #ef4444; color: white; border-color: #ef4444; }
.tab.active.vol { background: #6366f1; color: white; border-color: #6366f1; }

/* Form */
.res-form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  color: white;
}

.res-form input, .res-form select {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

/* Cards */
.res-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 16px;
  padding: 1.5rem;
  transition: transform 0.2s;
}

.res-card:hover { 
  transform: translateY(-5px); 
  background: rgba(255, 255, 255, 0.1);
}

.res-card.fulfilled { opacity: 0.6; }

.card-details {
  background: rgba(0, 0, 0, 0.3);
  color: #cbd5e1;
  padding: 0.8rem;
  border-radius: 8px;
}

.card-top .time { color: #94a3b8; }
.empty { text-align: center; color: #64748b; font-size: 1.2rem; }
"""

    # 3. ADMIN CSS (Dashboard)
    admin_css = """.admin-login {
  background: transparent; /* Use global dark bg */
}

.admin-panel {
  min-height: 100vh;
  background: transparent;
  color: white;
}

.admin-header {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.table-container {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

table { color: white; }

th { 
  background: rgba(0, 0, 0, 0.3); 
  color: #cbd5e1; 
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

td { border-bottom: 1px solid rgba(255,255,255,0.05); }

.verified-row { background: rgba(16, 185, 129, 0.1); }
"""

    # Write the files
    files = {
        'Auth.css': auth_css,
        'Resources.css': resources_css,
        'AdminPanel.css': admin_css
    }

    for filename, content in files.items():
        with open(os.path.join(pages_path, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {filename}")

    print("\n✨ Theme Unification Complete!")
    print("Your Login, Resources, and Admin pages are now Dark Mode & Glassmorphic.")


if __name__ == "__main__":
    unify_theme()