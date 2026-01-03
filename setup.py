#!/usr/bin/env python3
"""
PseudoQui Project Setup Script
Automated setup for backend and frontend
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def setup_backend():
    """Setup Python backend"""
    print_header("Setting up Backend")
    
    backend_dir = "backend"
    
    if not os.path.exists(backend_dir):
        print(f"Backend directory not found: {backend_dir}")
        return False
    
    print("Installing Python dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=backend_dir):
        print("Failed to install dependencies")
        return False
    
    print("Backend setup complete!")
    return True

def setup_frontend():
    """Setup Node.js frontend"""
    print_header("Setting up Frontend")
    
    frontend_dir = "frontend"
    
    if not os.path.exists(frontend_dir):
        print(f"Frontend directory not found: {frontend_dir}")
        return False
    
    # Check if node is installed
    try:
        subprocess.run("node --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Node.js is not installed. Please install Node.js first.")
        return False
    
    print("Installing npm dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        print("Failed to install dependencies")
        return False
    
    print("Frontend setup complete!")
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating directories")
    
    dirs = [
        "backend/data",
        "backend/tests"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created: {dir_path}")

def main():
    """Main setup function"""
    print_header("PseudoQui Project Setup")
    print("Welcome to PseudoQui Setup!")
    print("This script will set up both backend and frontend.")
    
    # Create directories
    create_directories()
    
    # Setup backend
    if not setup_backend():
        print("\nBackend setup failed. Please check your Python installation.")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("\nFrontend setup failed. Please check your Node.js installation.")
        return False
    
    print_header("Setup Complete!")
    print("""
Now you can run the project:

1. Start the backend:
   cd backend
   python run.py
   
   The API will be available at: http://localhost:5000

2. In another terminal, start the frontend:
   cd frontend
   npm start
   
   The app will open at: http://localhost:3000

For testing the backend:
   cd backend
   python -m unittest discover tests/ -v

Enjoy playing PseudoQui!
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
