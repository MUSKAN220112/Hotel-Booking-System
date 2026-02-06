"""
Configuration settings for SmartStay Hotel Booking System
"""

import os
from datetime import timedelta

# Flask Configuration
DEBUG = os.environ.get('FLASK_ENV') == 'development'
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database Configuration
DATABASE = os.environ.get('DATABASE_PATH', 'hotel_booking.db')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DATABASE}')

# Server Configuration
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Application Settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files

# Room Settings
DEFAULT_ROOM_PRICE = 100.00
MIN_BOOKING_DAYS = 1
MAX_BOOKING_DAYS = 365

# Email Configuration (optional)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')

# Admin Settings
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@smartstay.com')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
