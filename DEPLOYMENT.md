# SmartStay Hotel Booking System - Deployment Guide

## Quick Start Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python hotel.py
   ```

3. **Access the application:**
   Open browser to `http://localhost:5000`

## Deploy to Render

### Step 1: Prepare Your Repository
- Push your code to GitHub (or GitLab/Bitbucket)
- Ensure all files are committed

### Step 2: Create New Service on Render

1. Go to [render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Fill in the following:
   - **Name**: `smartstay-hotel-booking`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn hotel:app`
   - **Instance Type**: Free (or Starter)

### Step 3: Set Environment Variables

In Render dashboard:
1. Go to your service settings
2. Click "Environment"
3. Add the following variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=generate-a-random-secret-key-here
   DATABASE_PATH=/tmp/hotel_booking.db
   PORT=5000
   ```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete (5-10 minutes)
3. Your app will be live at: `https://your-service-name.onrender.com`

## Important Notes for Render

- **Database**: SQLite database is reset on each deploy. For production, consider using PostgreSQL
- **Static Files**: CSS and JS files are served correctly from the `/static` folder
- **CORS**: Already configured for web access

## Features Included

- ✅ User Authentication (Register/Login)
- ✅ Room Booking System
- ✅ Admin Dashboard
- ✅ Room Management
- ✅ Booking History
- ✅ Responsive Design
- ✅ Production-ready

## Default Admin Account (Create First)

Since the system uses SQLite, create your first admin account by:
1. Registering as a normal user
2. Access the database and manually update the user role to 'admin'
3. Or modify the `init_db()` function to create a default admin

## Troubleshooting

### Issue: "Cannot import name 'X'" 
**Solution**: Run `pip install -r requirements.txt` again

### Issue: Database errors
**Solution**: Check the DATABASE_PATH environment variable points to a writable location

### Issue: Static files not loading
**Solution**: Ensure Flask is serving static files from `/static` directory

## Database Migration for Production

For production use, migrate to PostgreSQL:

```python
# Install psycopg2
pip install psycopg2-binary

# Update database connection in hotel.py
import psycopg2
# ... use psycopg2 instead of sqlite3
```

Then add DATABASE_URL to Render environment.

## Support

For issues with Render deployment, visit: https://render.com/docs
