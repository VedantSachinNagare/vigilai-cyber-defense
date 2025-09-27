# VigilAI Cyber Defense System - Setup Guide

This guide will walk you through setting up the VigilAI Cyber Defense System on your local machine.

## Quick Start

### 1. Prerequisites

Ensure you have the following installed:

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads)
- **Text Editor**: VS Code, PyCharm, or any preferred editor

### 2. Project Setup

```bash
# Clone the repository (if using Git)
git clone <repository-url>
cd vigilai-cyber-defense

# Or extract the project files to a folder
# Navigate to the project directory
cd vigilai-cyber-defense
```

### 3. Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit .env file with your settings
# The default settings should work for local development
```

### 6. Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser
# Follow the prompts to create an admin user
```

### 7. Load Sample Data

```bash
# Load sample emails for testing
python manage.py load_sample_emails

# Load sample network logs and threats
python manage.py load_sample_logs --user admin
```

### 8. Run the Application

```bash
python manage.py runserver
```

Open your browser and navigate to: `http://127.0.0.1:8000`

## Detailed Setup Instructions

### Step 1: Python Environment

1. **Install Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

### Step 2: Install Dependencies

The `requirements.txt` file contains all necessary packages:

```bash
pip install -r requirements.txt
```

Key packages include:
- Django 4.2.7
- Transformers (for DistilBERT)
- Scikit-learn (for ML models)
- Pandas, NumPy (for data processing)
- Django REST Framework (for API)

### Step 3: Database Configuration

1. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123` (or your choice)

### Step 4: Load Sample Data

1. **Load Sample Emails**
   ```bash
   python manage.py load_sample_emails
   ```
   This loads 10 sample emails (legitimate, spam, phishing) for testing.

2. **Load Sample Network Data**
   ```bash
   python manage.py load_sample_logs --user admin
   ```
   This creates sample network logs and threats for testing.

### Step 5: Start the Application

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Testing the Application

### 1. Access the Dashboard

- Navigate to `http://127.0.0.1:8000`
- Login with your admin credentials
- You should see the main dashboard with statistics

### 2. Test Email Classification

1. Go to "Email Classifier" section
2. Try the sample emails provided
3. Test with your own email content
4. Verify classification results and confidence scores

### 3. Test Network Detection

1. Go to "Network Detection" section
2. View the sample threats and logs
3. Use the detection controls
4. Analyze the threat statistics

### 4. Explore Analytics

1. Go to "Analytics" section
2. View trend charts and statistics
3. Analyze threat patterns
4. Review detection metrics

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Use a different port
   python manage.py runserver 8001
   ```

2. **Database Errors**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   ```

3. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

4. **Permission Errors**
   ```bash
   # On Linux/macOS, ensure proper permissions
   chmod +x manage.py
   ```

### Python Version Issues

If you encounter Python version issues:

```bash
# Check Python version
python --version

# Use specific Python version
python3.8 -m venv venv
python3.8 manage.py runserver
```

### Virtual Environment Issues

If virtual environment activation fails:

```bash
# On Windows PowerShell
venv\Scripts\Activate.ps1

# On Windows Command Prompt
venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

## Development Setup

### For Developers

1. **Install Development Dependencies**
   ```bash
   pip install -r requirements-dev.txt  # If available
   ```

2. **Enable Debug Mode**
   ```python
   # In settings.py
   DEBUG = True
   ```

3. **Use Django Admin**
   - Navigate to `http://127.0.0.1:8000/admin`
   - Login with superuser credentials
   - Manage data and view models

### Code Structure

```
vigilai-cyber-defense/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── SETUP.md                 # This setup guide
├── vigilai/                 # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI configuration
├── email_classifier/        # Email classification app
├── network_detection/       # Network detection app
├── dashboard/               # Dashboard app
└── templates/               # HTML templates
```

## Production Deployment

### Basic Production Setup

1. **Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database**
   - Consider using PostgreSQL for production
   - Update DATABASES setting in settings.py

4. **Web Server**
   - Use Gunicorn or similar WSGI server
   - Configure reverse proxy (Nginx)

### Security Considerations

1. **Change Default Secret Key**
2. **Use HTTPS in production**
3. **Configure proper CORS settings**
4. **Set up proper logging**
5. **Use environment variables for sensitive data**

## Support

If you encounter issues:

1. Check this setup guide
2. Review the README.md file
3. Check Django documentation
4. Verify Python and package versions
5. Ensure all dependencies are installed

## Next Steps

After successful setup:

1. Explore the dashboard
2. Test email classification
3. Analyze network threats
4. Review the API endpoints
5. Customize the system for your needs

The system is now ready for use and testing!
