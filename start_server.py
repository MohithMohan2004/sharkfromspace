#!/usr/bin/env python3
"""
Sharks from Space - Integrated Frontend & Backend Startup Script
This script starts the Flask server that serves both the frontend and backend API.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        import folium
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r sharkfromspace/requirements.txt")
        return False

def install_dependencies():
    """Install dependencies if missing"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "sharkfromspace/requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("🦈 Starting Sharks from Space Server...")
    print("=" * 50)
    
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    # Start the Flask app
    try:
        from app import app
        print("🚀 Server starting on http://localhost:5000")
        print("📊 API endpoints available at /api/*")
        print("🌐 Frontend pages available at /")
        print("🦈 Shark Tracker available at /tracker.html")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using Sharks from Space!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🦈 Sharks from Space - Frontend & Backend Integration")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n🔧 Attempting to install missing dependencies...")
        if not install_dependencies():
            print("❌ Please install dependencies manually and try again.")
            sys.exit(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
