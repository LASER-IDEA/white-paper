import ast
import sys
import os
import importlib

def check_syntax(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        print(f"Syntax check passed for {filepath}")
        return True
    except SyntaxError as e:
        print(f"Syntax error in {filepath}: {e}")
        return False

def check_imports():
    required = [
        "streamlit", "streamlit_echarts", "pandas",
        "pyecharts", "openai"
    ]
    missing = []
    for req in required:
        try:
            importlib.import_module(req)
        except ImportError:
            missing.append(req)

    if missing:
        print(f"Missing dependencies: {missing}")
        return False
    print("All key dependencies found.")
    return True

def main():
    app_path = os.path.join(os.path.dirname(__file__), "../src/app.py")
    if not check_syntax(app_path):
        sys.exit(1)

    if not check_imports():
        sys.exit(1)

    print("App verification successful.")

if __name__ == "__main__":
    main()
