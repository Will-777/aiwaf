# AI-WAF Django Installation Guide

This guide helps you properly install AI-WAF in your Django project to avoid common setup errors.

## 🚨 Common Error Fix

**Error:** `RuntimeError: Model class aiwaf.models.FeatureSample doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.`

**Solution:** Follow the complete installation steps below.

## 📦 Step 1: Install AI-WAF

```bash
pip install aiwaf
```

## ⚙️ Step 2: Configure Django Settings

Add AI-WAF to your Django project's `settings.py`:

### **Required: Add to INSTALLED_APPS**

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'your_app',
    
    # AI-WAF (REQUIRED - must be in INSTALLED_APPS)
    'aiwaf',
]
```

### **Required: Basic Configuration**

```python
# AI-WAF Configuration
AIWAF_ACCESS_LOG = "/var/log/nginx/access.log"  # Path to your access log

# Optional: Choose storage mode
AIWAF_STORAGE_MODE = "csv"  # or "models" (default)
AIWAF_CSV_DATA_DIR = "aiwaf_data"  # For CSV mode
```

### **Required: Add Middleware**

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # AI-WAF Protection Middleware (add these)
    'aiwaf.middleware.IPAndKeywordBlockMiddleware',
    'aiwaf.middleware.RateLimitMiddleware',
    'aiwaf.middleware.AIAnomalyMiddleware',
    'aiwaf.middleware.HoneypotTimingMiddleware',
    'aiwaf.middleware.UUIDTamperMiddleware',
    
    # Optional: AI-WAF Request Logger
    'aiwaf.middleware_logger.AIWAFLoggerMiddleware',
]
```

## 🗄️ Step 3: Database Setup

### **Option A: Using Django Models (default)**

```bash
# Create migrations
python manage.py makemigrations aiwaf

# Apply migrations
python manage.py migrate
```

### **Option B: Using CSV Files (no database required)**

```python
# In settings.py
AIWAF_STORAGE_MODE = "csv"
AIWAF_CSV_DATA_DIR = "aiwaf_data"
```

No migrations needed! CSV files are created automatically.

## 🚀 Step 4: Test Installation

```bash
# Test the installation
python manage.py check

# Add a test IP exemption
python manage.py add_ipexemption 127.0.0.1 --reason "Testing"

# Check AI-WAF status
python manage.py aiwaf_logging --status
```

## 🔧 Step 5: Optional Configuration

### **Enable Built-in Request Logger**

```python
# settings.py
AIWAF_MIDDLEWARE_LOGGING = True
AIWAF_MIDDLEWARE_LOG = "aiwaf_requests.log"
AIWAF_MIDDLEWARE_CSV = True
```

### **Exempt Paths**

```python
# settings.py
AIWAF_EXEMPT_PATHS = [
    "/favicon.ico",
    "/robots.txt",
    "/static/",
    "/media/",
    "/health/",
    "/api/webhooks/",
]
```

### **AI Settings**

```python
# settings.py
AIWAF_AI_CONTAMINATION = 0.05  # AI sensitivity (5%)
AIWAF_MIN_FORM_TIME = 1.0      # Honeypot timing
AIWAF_RATE_MAX = 20            # Rate limiting
```

## 🎯 Step 6: Start Training

```bash
# Train the AI model (after some traffic)
python manage.py detect_and_train
```

## 🛠️ Troubleshooting

### **Error: Model not in INSTALLED_APPS**

**Problem:** AI-WAF models can't be loaded.

**Solutions:**
1. Add `'aiwaf'` to `INSTALLED_APPS` (required)
2. Run `python manage.py migrate` if using models
3. Use CSV mode: `AIWAF_STORAGE_MODE = "csv"`

### **Error: No module named 'aiwaf'**

**Problem:** AI-WAF not installed properly.

**Solution:**
```bash
pip install aiwaf
# or
pip install --upgrade aiwaf
```

### **Error: Access log not found**

**Problem:** `AIWAF_ACCESS_LOG` points to non-existent file.

**Solutions:**
1. Fix log path in settings
2. Enable middleware logger: `AIWAF_MIDDLEWARE_LOGGING = True`
3. Use CSV mode for built-in logging

### **Error: Permission denied on CSV files**

**Problem:** Can't write to CSV directory.

**Solutions:**
1. Check directory permissions
2. Change `AIWAF_CSV_DATA_DIR` to writable location
3. Run Django with proper user permissions

## 📁 File Structure After Installation

### **Models Mode:**
```
your_project/
├── manage.py
├── settings.py
├── db.sqlite3 (contains aiwaf tables)
└── aiwaf_requests.log (if middleware logging enabled)
```

### **CSV Mode:**
```
your_project/
├── manage.py  
├── settings.py
├── aiwaf_data/              # Created automatically
│   ├── blacklist.csv
│   ├── exemptions.csv  
│   ├── keywords.csv
│   └── access_samples.csv
└── aiwaf_requests.log       # Middleware logger
```

## ✅ Verification Checklist

- [ ] `aiwaf` added to `INSTALLED_APPS`
- [ ] `AIWAF_ACCESS_LOG` configured
- [ ] Middleware added to `MIDDLEWARE`
- [ ] Migrations run (if using models mode)
- [ ] `python manage.py check` passes
- [ ] Test command works: `python manage.py add_ipexemption 127.0.0.1`

## 🏃‍♂️ Quick Start (Minimal Setup)

```python
# settings.py - Minimal configuration

INSTALLED_APPS = [
    # ... existing apps ...
    'aiwaf',  # Required
]

MIDDLEWARE = [
    # ... existing middleware ...
    'aiwaf.middleware.IPAndKeywordBlockMiddleware',  # Basic protection
]

# Choose one:
AIWAF_ACCESS_LOG = "/var/log/nginx/access.log"  # Use server logs
# OR
AIWAF_MIDDLEWARE_LOGGING = True  # Use built-in logger
```

```bash
# Run migrations (if using models)
python manage.py migrate

# Start protecting!
python manage.py runserver
```

That's it! AI-WAF is now protecting your Django application.
