#!/usr/bin/env python3
"""
Convenience script to run the Python Streamlit application.
This script changes to the python directory and runs the Streamlit app.
"""

import os
import sys
import subprocess

def main():
    # Change to python directory
    python_dir = os.path.join(os.path.dirname(__file__), 'python')
    os.chdir(python_dir)

    # Run streamlit app
    cmd = [sys.executable, '-m', 'streamlit', 'run', 'src/app.py']
    print("Starting Streamlit application...")
    print(f"Working directory: {python_dir}")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running application: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())