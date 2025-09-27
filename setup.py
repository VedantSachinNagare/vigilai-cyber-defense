#!/usr/bin/env python
"""
Setup script for VigilAI Cyber Defense System
"""
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print("Setting up virtual environment...")
    
    # Check if virtual environment already exists
    if os.path.exists('venv'):
        print("Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command('python -m venv venv', 'Creating virtual environment'):
        return False
    
    print("Virtual environment created successfully")
    return True

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        pip_path = 'venv/bin/pip'
    
    if not run_command(f'{pip_path} install -r requirements.txt', 'Installing Python packages'):
        return False
    
    print("Dependencies installed successfully")
    return True

def setup_database():
    """Set up the database"""
    print("Setting up database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vigilai.settings')
    django.setup()
    
    # Create migrations
    if not run_command('python manage.py makemigrations', 'Creating database migrations'):
        return False
    
    # Apply migrations
    if not run_command('python manage.py migrate', 'Applying database migrations'):
        return False
    
    print("Database setup completed successfully")
    return True

def create_superuser():
    """Create a superuser account"""
    print("Creating superuser account...")
    
    # Check if superuser already exists
    try:
        from django.contrib.auth.models import User
        if User.objects.filter(is_superuser=True).exists():
            print("Superuser already exists")
            return True
    except:
        pass
    
    # Create superuser
    print("Creating superuser account (admin/admin123)")
    try:
        from django.contrib.auth.models import User
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✓ Superuser created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create superuser: {e}")
        return False

def load_sample_data():
    """Load sample data for testing"""
    print("Loading sample data...")
    
    # Load sample emails
    if not run_command('python manage.py load_sample_emails', 'Loading sample emails'):
        return False
    
    # Load sample network logs
    if not run_command('python manage.py load_sample_logs --user admin', 'Loading sample network data'):
        return False
    
    print("Sample data loaded successfully")
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("VigilAI Cyber Defense System - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version} detected")
    
    # Setup steps
    steps = [
        ("Virtual Environment", setup_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Database", setup_database),
        ("Superuser", create_superuser),
        ("Sample Data", load_sample_data),
    ]
    
    for step_name, step_function in steps:
        print(f"\n--- {step_name} ---")
        if not step_function():
            print(f"✗ Setup failed at step: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the application:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("2. Run the development server:")
    print("   python manage.py runserver")
    print("3. Open your browser and go to: http://127.0.0.1:8000")
    print("4. Login with: admin / admin123")
    print("\nFor more information, see README.md and SETUP.md")

if __name__ == '__main__':
    main()
