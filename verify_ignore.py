import os

def verify_ignore():
    content = """node_modules/
frontend/node_modules/
backend/node_modules/
build/
.env
"""
    with open('.gitignore', 'w') as f:
        f.write(content)
    print("✅ .gitignore fixed.")

if __name__ == "__main__":
    verify_ignore()
