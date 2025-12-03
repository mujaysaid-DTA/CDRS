import os


def link_chat_route():
    base_path = os.getcwd()
    app_jsx_path = os.path.join(base_path, 'frontend', 'src', 'App.jsx')

    print("🔗 Linking Chat Page to App.jsx...")

    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Import if missing
    if "import Chat from" not in content:
        # Find the last import and add Chat after it
        content = content.replace("import Register from './pages/Register';",
                                  "import Register from './pages/Register';\nimport Chat from './pages/Chat';")
        print("   ✅ Added Import statement")

    # 2. Add Route if missing
    if '<Route path="/chat"' not in content:
        # Add the route before the closing </Routes> tag
        content = content.replace("</Routes>",
                                  '  <Route path="/chat" element={<Chat />} />\n      </Routes>')
        print("   ✅ Added Route definition")

    # 3. Add Navigation Button (Optional - adds it to the Home screen)
    if '/chat' not in content and 'Link to="/chat"' not in content:
        # Add a button to the homepage hero section
        content = content.replace('<Link to="/login" className="cta-button secondary">Login</Link>',
                                  '<Link to="/login" className="cta-button secondary">Login</Link>\n            <Link to="/chat" className="cta-button primary">🔴 Live Chat</Link>')
        print("   ✅ Added 'Live Chat' button to Home Page")

    with open(app_jsx_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n✨ App.jsx updated! You can now visit /chat.")


if __name__ == "__main__":
    link_chat_route()