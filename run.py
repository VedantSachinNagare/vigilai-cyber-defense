#!/usr/bin/env python
"""
Quick start script for VigilAI Cyber Defense System
"""
import os
import sys
import subprocess

def main():
    """Start the Django development server"""
    print("Starting VigilAI Cyber Defense System...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Virtual environment not found. Please run setup.py first.")
        sys.exit(1)
    
    # Determine the correct python path
    if os.name == 'nt':  # Windows
        python_path = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_path = 'venv/bin/python'
    
    # Start the development server
    try:
        print("Starting Django development server...")
        print("Open your browser and go to: http://127.0.0.1:8000")
        print("Login with: admin / admin123")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([python_path, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
