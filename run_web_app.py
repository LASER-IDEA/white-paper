#!/usr/bin/env python3
"""
Convenience script to run the TypeScript React application.
This script changes to the web directory and runs the development server.
"""

import os
import sys
import subprocess

def main():
    # Change to web directory
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    os.chdir(web_dir)
    print(f"Current working directory: {os.getcwd()}")

    # Check if npm is available
    try:
        subprocess.run(['npm.cmd', '--version'], check=True, capture_output=True)
        package_manager = 'npm.cmd'
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['yarn.cmd', '--version'], check=True, capture_output=True)
            package_manager = 'yarn.cmd'
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Neither npm nor yarn is installed.")
            return 1

    # Install dependencies if node_modules doesn't exist
    if not os.path.exists('node_modules'):
        print("Installing dependencies...")
        subprocess.run([package_manager, 'install'], check=True)

    # Run development server
    print("Starting development server...")
    print(f"Working directory: {web_dir}")
    print(f"Package manager: {package_manager}")

    cmd = [package_manager, 'run', 'dev']
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nDevelopment server stopped by user.")
    except Exception as e:
        print(f"Error running development server: {e}")
        return 1

    return 0

if __name__ == '__main__':
    print("PATH:", os.environ.get("PATH"))
    sys.exit(main())