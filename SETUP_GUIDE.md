# SmartStay Hotel Booking System - Complete Setup Guide

**Made by: Muskan Chohan**

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Database Initialization](#database-initialization)
4. [Running the Application](#running-the-application)
5. [Testing the Features](#testing-the-features)
6. [Render Deployment](#render-deployment)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements:
- **Python**: 3.8 or higher (tested on 3.11+)
- **SQLite**: 3.30.0+ (usually bundled with Python)
- **Disk Space**: 500 MB
- **RAM**: 512 MB

### Recommended Setup:
- **Python**: 3.11.0
- **Virtual Environment**: Python venv or conda
- **Git**: For version control and deployment

---

## Local Development Setup

### Step 1: Clone/Download the Project

```bash
cd /home/mspl/Hotel\ Booking\ System
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Expected Output:
```
Successfully installed:
- Flask 2.3.3
- Werkzeug 2.3.7
- python-dotenv 1.0.0
- gunicorn 21.2.0
- Pillow 10.0.0
- WTForms 3.0.1
- Flask-WTF 1.1.1
- email-validator 2.0.0
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=hotel.py
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE=hotel_booking.db

# Server
HOST=0.0.0.0
PORT=5000
```

---

## Database Initialization

### Step 1: Automatic Initialization

The database is automatically created when you first run the application. The application will:

1. Check if the database file exists
2. Create all tables with proper schema if it doesn't exist
3. Create necessary indexes
4. Initialize with sample data (optional)

### Step 2: Add Sample Data

Run the sample data script to populate the database with demo data:

```bash
python sample_data.py
```

**Output:**
```
✓ Sample data created successfully!

Created:
- 5 sample users (including admin and guest accounts)
- 5 sample hotels with locations
- 11 sample rooms with various types
- 3 sample bookings for testing
- 3 sample reviews

Admin Credentials:
- Email: admin@hotel.com
- Password: admin123

Guest Test Account:
- Email: muskan@smartstay.com
- Password: muskan123
```

### Step 3: Verify Database

```bash
sqlite3 hotel_booking.db ".tables"
```

**Expected Output:**
```
users    hotels    rooms    bookings    reviews
```

Check table structure:
```bash
sqlite3 hotel_booking.db ".schema users"
```

---

## Running the Application

### Development Mode

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the application
python hotel.py
```

**Expected Output:**
```
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### Production Mode (Gunicorn)

```bash
gunicorn hotel:app --workers 4 --bind 0.0.0.0:5000
```

---

## Testing the Features

### 1. User Registration

**URL:** `http://localhost:5000/register`

**Test Case:**
- Fill in: Name, Email, Password, Confirm Password
- Click "Register"
- Expected: Redirected to login page with success message

### 2. User Login

**URL:** `http://localhost:5000/login`

**Test Cases:**

**Admin Login:**
- Email: `admin@hotel.com`
- Password: `admin123`

**Guest Login:**
- Email: `muskan@smartstay.com`
- Password: `muskan123`

### 3. Search Hotels & Rooms

**URL:** `http://localhost:5000/search`

**Test Case:**
- Select check-in date (tomorrow or later)
- Select check-out date (after check-in)
- Enter city (optional)
- Click Search
- Expected: Filtered results showing available rooms

**Filter Options:**
- Price range: ₹2000 - ₹15000
- Room type: Single, Double, Suite, Penthouse
- City: All available cities

### 4. View Room Details

**Test Case:**
- From search results, click on any room card
- Expected: Detailed page showing:
  - Room images
  - Amenities list
  - Guest reviews
  - Booking button

### 5. Make a Booking

**URL:** `http://localhost:5000/room/<room_id>`

**Test Case:**
- Click "Book Now" button
- Fill in check-in and check-out dates
- Enter number of guests
- Add special requests (optional)
- Click "Confirm Booking"
- Expected: Confirmation page with unique booking ID

**Booking ID Format:** `BK20260206ABC123`

### 6. View My Bookings

**URL:** `http://localhost:5000/my-bookings`

**Test Case:**
- View all your bookings
- See booking details and status
- Cancel a booking (status changes to 'cancelled')

### 7. User Profile

**URL:** `http://localhost:5000/profile`

**View:**
- Your profile information
- Booking statistics
- Account details

### 8. Admin Dashboard

**URL:** `http://localhost:5000/admin`

**Requirements:** Must be logged in as admin

**Features:**

#### Dashboard Overview
- Total bookings count
- Total revenue
- New bookings (last 7 days)
- Occupancy rate

#### Hotels Management
- **URL:** `/admin/hotels`
- Add new hotels
- Edit hotel information
- View all hotels

#### Rooms Management
- **URL:** `/admin/rooms`
- Add rooms to hotels
- Edit room details
- Change room status
- Set pricing

#### Bookings Management
- **URL:** `/admin/bookings`
- View all bookings
- See booking details
- Track booking status

### 9. API Endpoints (for AJAX)

#### Check Room Availability
```bash
POST /api/check-availability
Content-Type: application/json

{
    "room_id": 1,
    "check_in": "2026-02-10",
    "check_out": "2026-02-12"
}
```

**Response:**
```json
{
    "available": true,
    "message": "Room is available for selected dates"
}
```

#### Health Check
```bash
GET /api/health
```

**Response:**
```json
{
    "status": "healthy",
    "database": "connected",
    "version": "1.0.0"
}
```

---

## Render Deployment

### Step 1: Prepare Repository

```bash
# Initialize git repository (if not already)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: SmartStay Hotel Booking System"
```

### Step 2: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/yourusername/hotel-booking.git

# Push code
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure deployment:
   - **Name:** hotel-booking-system
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn hotel:app`
5. Add environment variable:
   - **Key:** SECRET_KEY
   - **Value:** Generate a strong secret key
6. Click "Deploy"

### Step 4: Post-Deployment

After deployment:

```bash
# Access your app
https://hotel-booking-system.render.com

# Initialize database on server
# (Database will auto-initialize on first run)
```

### Render Dashboard Features

- **Logs:** View application logs in real-time
- **Metrics:** Monitor CPU, memory usage
- **Environment:** Manage environment variables
- **Deploy:** Manual or automatic deployments

---

## Troubleshooting

### Issue 1: "No such column: is_available"

**Cause:** Old database schema

**Solution:**
```bash
# Backup old database
mv hotel_booking.db hotel_booking.db.backup

# Run application (new database created)
python hotel.py

# Load sample data
python sample_data.py
```

### Issue 2: "Module not found" errors

**Cause:** Missing dependencies

**Solution:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Verify installation
pip list
```

### Issue 3: Database locked error

**Cause:** Multiple processes accessing database

**Solution:**
```bash
# Close all instances of the application
# Delete lock file if exists
rm hotel_booking.db-journal

# Restart application
python hotel.py
```

### Issue 4: Port 5000 already in use

**Cause:** Another application using port 5000

**Solution:**
```bash
# Use different port
FLASK_ENV=development python hotel.py --port=5001

# Or kill the process using port 5000
# macOS/Linux:
lsof -ti:5000 | xargs kill

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue 5: Image upload not working

**Cause:** Missing uploads directory

**Solution:**
```bash
# Create uploads directory
mkdir -p static/uploads

# Ensure directory is writable
chmod 755 static/uploads
```

### Issue 6: CSRF token errors on forms

**Cause:** Session secret not configured

**Solution:**
```bash
# Edit .env file
SECRET_KEY=your-random-secret-key-here

# Restart application
python hotel.py
```

---

## Database Backup

### Create Backup

```bash
# Simple copy
cp hotel_booking.db hotel_booking.db.backup

# Or with timestamp
cp hotel_booking.db "hotel_booking_$(date +%Y%m%d_%H%M%S).db"
```

### Restore Backup

```bash
# Stop application first
# Then restore
mv hotel_booking.db.backup hotel_booking.db

# Restart application
python hotel.py
```

### Export to CSV

```bash
# Hotels data
sqlite3 hotel_booking.db ".mode csv" ".output hotels.csv" "SELECT * FROM hotels;"

# Bookings data
sqlite3 hotel_booking.db ".mode csv" ".output bookings.csv" "SELECT * FROM bookings;"
```

---

## Performance Tips

1. **Database Optimization:**
   - Regularly analyze database: `ANALYZE;`
   - Rebuild indexes: `REINDEX;`

2. **Caching:**
   - Enable browser caching for static files
   - Use CDN for images in production

3. **Scaling:**
   - For high traffic, migrate to PostgreSQL
   - Implement Redis for session management
   - Use load balancing on Render

4. **Monitoring:**
   - Check Render logs regularly
   - Monitor response times
   - Track database queries

---

## Support & Documentation

- **Database Schema:** See `DATABASE_SCHEMA.md`
- **Deployment Details:** See `DEPLOYMENT.md`
- **API Documentation:** See `API.md`
- **Bug Reports:** Create an issue in GitHub
- **Feature Requests:** Open a discussion

---

## License & Credits

**Made by: Muskan**

This project is built for educational and commercial use with proper MVC architecture, responsive design, and production-ready deployment configuration.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial release with all core features |

---

**Last Updated:** February 2026
