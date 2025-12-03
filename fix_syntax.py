import os
import re


def fix_syntax():
    base_path = os.getcwd()
    pages_dir = os.path.join(base_path, 'frontend', 'src', 'pages')

    # Files listed in your error log
    files = [
        'AdminPanel.jsx',
        'IncidentList.jsx',
        'IncidentMap.jsx',
        'Login.jsx',
        'Register.jsx',
        'ReportIncident.jsx',
        'Resources.jsx'
    ]

    print("🔧 Fixing Syntax Errors (Closing quotes)...")

    for filename in files:
        filepath = os.path.join(pages_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # REGEX EXPLANATION:
            # We look for strings that start with: ` (backtick) + ${API_BASE_URL}
            # But end with: ' (single quote)
            # We replace the ending ' with ` (backtick)

            new_content = re.sub(
                r'`\$\{API_BASE_URL\}([^`\']*)\'',
                r'`${API_BASE_URL}\1`',
                content
            )

            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"   ✅ Fixed typos in {filename}")
            else:
                print(f"   (No typos found in {filename})")

    print("\n✨ Syntax repairs complete.")


if __name__ == "__main__":
    fix_syntax()