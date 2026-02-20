#!/usr/bin/env python3
"""
LAEV-Agents Demo Launcher

This script sets up the environment and launches the demo with your choice of UI.

Usage:
    python run_demo.py              # Interactive mode
    python run_demo.py streamlit    # Launch Streamlit UI
    python run_demo.py gradio       # Launch Gradio UI
"""

import sys
import subprocess
import os
import argparse
from pathlib import Path

def check_dependencies(ui_type: str = "both"):
    """Check if required dependencies are installed."""
    if ui_type == "streamlit":
        required = ['streamlit', 'pandas', 'numpy', 'pyecharts']
    elif ui_type == "gradio":
        required = ['gradio', 'pandas', 'numpy', 'pyecharts']
    else:
        required = ['streamlit', 'gradio', 'pandas', 'numpy', 'pyecharts']
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_dependencies():
    """Install missing dependencies."""
    print("Installing dependencies...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])

def setup_environment():
    """Setup environment variables and paths."""
    # Add python/src to path
    project_root = Path(__file__).parent.parent
    python_src = project_root / "python" / "src"
    
    if str(python_src) not in sys.path:
        sys.path.insert(0, str(python_src))
    
    # Check for .env file
    env_file = project_root / ".env"
    if env_file.exists():
        print(f"✓ Found .env file at {env_file}")
    else:
        print(f"⚠ Warning: No .env file found at {env_file}")
        print("  Please create one with your API keys (DEEPSEEK_API_KEY, etc.)")

def launch_streamlit():
    """Launch Streamlit demo."""
    print("\n🚀 Launching Streamlit demo...")
    print("   URL: http://localhost:8501")
    print("   Press Ctrl+C to stop\n")
    
    app_file = Path(__file__).parent / "app.py"
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_file),
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.serverAddress", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped.")

def launch_gradio():
    """Launch Gradio demo."""
    print("\n🚀 Launching Gradio demo...")
    print("   URL: http://localhost:7860")
    print("   Press Ctrl+C to stop\n")
    
    app_file = Path(__file__).parent / "app_gradio.py"
    
    try:
        subprocess.run([sys.executable, str(app_file)])
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped.")

def interactive_menu():
    """Show interactive menu for UI selection."""
    print("\n📱 Select UI Framework:")
    print("   1. Streamlit (Modern, feature-rich)")
    print("   2. Gradio (Simple, compatible)")
    print("   3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        return "streamlit"
    elif choice == "2":
        return "gradio"
    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice, defaulting to Streamlit")
        return "streamlit"

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LAEV-Agents Demo Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_demo.py           # Interactive mode
  python run_demo.py streamlit # Launch Streamlit
  python run_demo.py gradio    # Launch Gradio
        """
    )
    parser.add_argument(
        "ui",
        nargs="?",
        choices=["streamlit", "gradio"],
        help="UI framework to use (default: interactive mode)"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("LAEV-Agents Demo Launcher")
    print("="*70)
    
    # Determine UI type
    if args.ui:
        ui_type = args.ui
    else:
        ui_type = interactive_menu()
    
    # Check dependencies
    missing = check_dependencies(ui_type)
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        response = input("Install now? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("Please install manually: pip install -r requirements.txt")
            sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Launch selected UI
    if ui_type == "streamlit":
        launch_streamlit()
    elif ui_type == "gradio":
        launch_gradio()

if __name__ == "__main__":
    main()
