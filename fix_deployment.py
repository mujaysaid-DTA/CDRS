import os


def fix_deployment():
    base_path = os.getcwd()

    print("🧹 Creating .gitignore to block heavy files...")

    gitignore_content = """# Dependencies
node_modules/
backend/node_modules/
frontend/node_modules/

# Production
build/
dist/

# Environment variables
.env
.DS_Store
"""

    with open(os.path.join(base_path, '.gitignore'), 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

    print("✅ .gitignore created.")
    print("\n👇 NOW RUN THE COMMANDS BELOW IN YOUR TERMINAL 👇")


if __name__ == "__main__":
    fix_deployment()