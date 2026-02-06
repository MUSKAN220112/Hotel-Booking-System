# 🏨 SmartStay Hotel Booking System

**A Professional Hotel Booking Platform Built with Flask & SQLite**

**Made by: Muskan**

---

## 📋 Overview

SmartStay is a comprehensive hotel booking system designed for both guests and administrators. It provides a seamless booking experience with a professional UI, robust backend, and complete admin management features. The system is production-ready and Render-deployment optimized.

### Key Highlights
- ✅ **Professional UI** - Modern, responsive Bootstrap 5 design
- ✅ **Complete Features** - Registration, search, booking, reviews, admin panel
- ✅ **Clean Architecture** - MVC pattern with proper separation of concerns
- ✅ **Database** - SQLite with 5 normalized tables and indexes
- ✅ **Authentication** - Secure user registration and session management
- ✅ **Admin Dashboard** - Complete hotel and room management
- ✅ **Booking System** - Real-time availability checking with unique booking IDs
- ✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ✅ **Render Ready** - Configured for instant deployment

---

## 🚀 Quick Start

### 1. **Prerequisites**
```bash
Python 3.8+ (tested on 3.11.0)
Git
Virtual Environment (recommended)
```

### 2. **Setup Local Environment**

```bash
# Navigate to project directory
cd "Hotel Booking System"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize environment
cp .env.example .env

# Create database and load sample data
python sample_data.py

# Run application
python hotel.py
```

### 3. **Access Application**
```
Open: http://localhost:5000
Admin: admin@hotel.com / admin123
Guest: muskan@smartstay.com / muskan123
```

---

## 📁 Project Structure

```
Hotel Booking System/
├── hotel.py                    # Main Flask application (30+ routes)
├── config.py                   # Configuration settings
├── sample_data.py              # Sample data initialization script
├── requirements.txt            # Python dependencies
├── hotel_booking.db            # SQLite database
│
├── templates/                  # HTML Templates (13 files)
│   ├── base.html              # Base layout with navbar & footer
│   ├── index.html             # Homepage with hero section
│   ├── register.html          # User registration page
│   ├── login.html             # User login page
│   ├── search_results.html    # Hotel & room search results
│   ├── room_detail.html       # Individual room details
│   ├── hotel_detail.html      # Individual hotel details
│   ├── booking.html           # Booking form with price calculation
│   ├── profile.html           # User profile page
│   ├── my_bookings.html       # User's booking history
│   ├── admin_dashboard.html   # Admin overview & statistics
│   ├── admin_hotels.html      # Hotel management
│   ├── admin_rooms.html       # Room management
│   └── admin_bookings.html    # Booking management
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet (600+ lines)
│   ├── js/
│   │   └── main.js            # JavaScript functionality
│   └── images/                # Image assets
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── Procfile                   # Gunicorn startup command
├── runtime.txt                # Python version for Render
├── render.yaml                # Render deployment config
│
├── DATABASE_SCHEMA.md         # Database design documentation
├── API.md                     # Complete API documentation
├── SETUP_GUIDE.md             # Detailed setup instructions
├── DEPLOYMENT.md              # Render deployment guide
└── README.md                  # This file
```

---

## 🏗️ Architecture

### Frontend
- **Framework:** Bootstrap 5.3.0
- **Styling:** Custom CSS (600+ lines) with animations
- **JavaScript:** jQuery 3.6.4 for DOM manipulation
- **Icons:** Font Awesome 6.4.0
- **Animations:** AOS (Animate On Scroll) 2.3.1

### Backend
- **Framework:** Flask 2.3.3
- **Language:** Python 3.11.0
- **Database:** SQLite3
- **Security:** Werkzeug password hashing
- **Forms:** WTForms with Flask-WTF validation
- **Server:** Gunicorn (production)

### Database Schema
```
Users (1) ←──────────────→ (Many) Bookings
             (1) ←─────────────→ (Many) Rooms
                                    ↓
                               Hotels (1)
                                    ↓
                              (Many) Reviews
```

---

## 🔑 Core Features

### 1. **User Authentication**
- User registration with validation
- Secure login with password hashing
- Session management
- Role-based access control (Guest/Admin)
- Profile management

### 2. **Hotel & Room Management**
- Browse all available hotels
- View hotel details and locations
- Search hotels by city
- Filter rooms by price, type, capacity
- View detailed room information
- Real-time availability checking
- Amenities and features display

### 3. **Booking System**
- Date-based room search
- Availability verification (prevents double-booking)
- Price calculation (nights × per-night rate)
- Unique booking ID generation
- Special requests support
- Booking confirmation
- Booking history and status tracking
- Booking cancellation

### 4. **Reviews & Ratings**
- Guest reviews on rooms
- Star rating system (1-5)
- Review display on room pages
- Average rating calculation

### 5. **Admin Dashboard**
- Overview with key statistics
- Total bookings and revenue tracking
- Weekly bookings analysis
- Occupancy rate calculation
- Recent bookings table

### 6. **Admin Management**
- **Hotels:** Add, edit, view all hotels
- **Rooms:** Add rooms to hotels, manage pricing, update status
- **Bookings:** View all bookings, track status, view details
- **Users:** View registered users, manage access

### 7. **Search & Filter**
- Search by city
- Filter by date range
- Price range filtering
- Room type filtering
- Results with availability status

---

## 🗄️ Database Tables

### 1. **Users**
- ID, Name, Email (unique), Password (hashed), Phone, Role, Created At

### 2. **Hotels**
- ID, Name, Description, City, Address, Phone, Email, Rating, Image

### 3. **Rooms**
- ID, Hotel ID, Room Number, Type, Capacity, Price, Amenities, Status, Images

### 4. **Bookings**
- ID, Booking ID (unique), User ID, Room ID, Hotel ID, Check-in, Check-out, Guests, Total Price, Status, Special Requests

### 5. **Reviews**
- ID, User ID, Room ID, Hotel ID, Rating, Comment, Title

See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for detailed schema documentation.

---

## 🛣️ API Routes

### Public Routes
- `GET /` - Homepage
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /search` - Search hotels and rooms
- `GET /hotel/<id>` - Hotel details
- `GET /room/<id>` - Room details

### Authenticated Routes
- `GET /logout` - Logout
- `GET /profile` - User profile
- `GET /my-bookings` - User's bookings
- `POST /booking/<room_id>` - Create booking
- `POST /booking/<id>/cancel` - Cancel booking

### Admin Routes
- `GET /admin` - Admin dashboard
- `GET /admin/hotels` - Hotel management
- `POST /admin/hotels/add` - Add hotel
- `GET /admin/rooms` - Room management
- `POST /admin/rooms/add` - Add room
- `GET /admin/bookings` - Bookings management

### API Endpoints
- `POST /api/check-availability` - Check room availability
- `GET /api/health` - Health check

See [API.md](API.md) for complete API documentation.

---

## 🔐 Security Features

- ✅ Password hashing with Werkzeug
- ✅ CSRF protection with Flask-WTF
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ Input validation on all forms
- ✅ SQL injection prevention (parameterized queries)
- ✅ Email validation
- ✅ Secure error handling

---

## 📊 Sample Data

The system includes `sample_data.py` that populates:
- **5 Sample Users** (including admin and guest accounts)
- **5 Sample Hotels** (across different cities)
- **11 Sample Rooms** (with various types and prices)
- **3 Sample Bookings** (for demonstration)
- **3 Sample Reviews** (from guests)

Load sample data with:
```bash
python sample_data.py
```

---

## 🎨 UI/UX Features

### Design Highlights
- **Hero Section** - Eye-catching landing page with search bar
- **Responsive Grid** - Adapts to all screen sizes
- **Card-Based Layout** - Modern presentation of hotels/rooms
- **Status Badges** - Visual indicators for booking status
- **Form Validation** - Real-time feedback on form inputs
- **Animations** - Smooth transitions and hover effects
- **Dark Theme Options** - Customizable color schemes
- **Accessibility** - WCAG 2.1 compliant

### Mobile Responsive
- Desktop: Full-featured experience
- Tablet: Optimized layout
- Mobile: Touch-friendly interface

---

## 🚀 Deployment

### Local Development
```bash
python hotel.py
```

### Production with Gunicorn
```bash
gunicorn hotel:app --workers 4 --bind 0.0.0.0:5000
```

### Deploy to Render
1. Push code to GitHub
2. Connect repository to Render
3. Deploy using `render.yaml` configuration
4. Database auto-initializes on first run

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

---

## 📖 Documentation

- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Complete database design
- **[API.md](API.md)** - Comprehensive API reference
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup and testing guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Render deployment guide

---

## 🧪 Testing

### Manual Testing Checklist

**User Features:**
- [ ] Register new account
- [ ] Login with credentials
- [ ] View profile
- [ ] Search hotels/rooms
- [ ] Filter by price, city, type
- [ ] View room details
- [ ] Make a booking
- [ ] View booking confirmation
- [ ] Cancel booking
- [ ] Logout

**Admin Features:**
- [ ] Login as admin
- [ ] View admin dashboard
- [ ] Add new hotel
- [ ] Add new room
- [ ] View all bookings
- [ ] Manage room status
- [ ] View statistics

### Test Accounts

```
Admin Account:
- Email: admin@hotel.com
- Password: admin123

Guest Account:
- Email: muskan@smartstay.com
- Password: muskan123
```

---

## 🐛 Troubleshooting

### Issue: Database errors on startup
**Solution:** Delete `hotel_booking.db` and run `python sample_data.py`

### Issue: Port 5000 already in use
**Solution:** Use different port: `python hotel.py --port=5001`

### Issue: Module not found errors
**Solution:** Reinstall dependencies: `pip install -r requirements.txt`

See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) for more troubleshooting tips.

---

## 📦 Dependencies

```
Flask==2.3.3
Werkzeug==2.3.7
python-dotenv==1.0.0
gunicorn==21.2.0
Pillow==10.0.0
WTForms==3.0.1
Flask-WTF==1.1.1
email-validator==2.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📈 Performance Optimization

- **Database Indexes** - 5 indexes on frequently queried columns
- **Lazy Loading** - Load images on-demand
- **Caching** - Browser caching for static files
- **Minification** - Optimized CSS and JavaScript
- **Query Optimization** - Efficient SQL queries with joins

---

## 🔄 Future Enhancements

- [ ] Email confirmation for bookings
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Real-time notifications (WebSocket)
- [ ] Multi-language support (i18n)
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] GraphQL API
- [ ] Redis caching
- [ ] Two-factor authentication
- [ ] Social login integration

---

## 💡 Best Practices Implemented

✅ **Code Organization**
- Modular route handlers
- Separation of concerns
- Helper functions and decorators

✅ **Database**
- Normalized schema (3NF)
- Proper foreign keys and constraints
- Indexed columns for performance

✅ **Security**
- Input validation and sanitization
- Password hashing
- CSRF protection
- Session management

✅ **User Experience**
- Responsive design
- Error handling with user-friendly messages
- Form validation with feedback
- Loading indicators

✅ **Documentation**
- Code comments and docstrings
- Comprehensive README
- API documentation
- Setup guides

---

## 📝 License & Credits

**Made by: Muskan**

This project is built for educational and commercial use with professional-grade architecture, security, and deployment capabilities.

---

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For support, questions, or bug reports:
- Open an issue on GitHub
- Contact: muskan.dev@example.com
- Documentation: See the docs folder

---

## 🎯 Project Statistics

- **Lines of Code:** ~2,500+
- **HTML Templates:** 13 files
- **Database Tables:** 5 normalized tables
- **API Endpoints:** 25+ routes
- **CSS Styling:** 600+ lines
- **JavaScript:** 300+ lines
- **Documentation:** 4 comprehensive guides

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial release with all core features |

---

## 🏆 Key Achievements

✅ Professional-grade hotel booking platform
✅ Clean, maintainable code architecture
✅ Comprehensive documentation
✅ Production-ready deployment configuration
✅ Responsive, modern UI/UX
✅ Complete feature set matching real platforms
✅ Secure authentication and authorization
✅ Database optimization with indexes

---

**Made with ❤️ by Muskan**

**Last Updated:** February 2026

---

### Quick Navigation
- 🚀 [Quick Start](#-quick-start)
- 📁 [Project Structure](#-project-structure)
- 🔑 [Core Features](#-core-features)
- 🗄️ [Database Tables](#-database-tables)
- 🛣️ [API Routes](#-api-routes)
- 🚀 [Deployment](#-deployment)
- 📖 [Documentation](#-documentation)
