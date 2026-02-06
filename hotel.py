"""
SmartStay Hotel Booking System
A professional hotel booking platform with user authentication, room management, and booking system
Made by Muskan
"""

import os
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Database configuration
DATABASE = os.environ.get('DATABASE_PATH', 'hotel_booking.db')

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with complete schema"""
    conn = get_db_connection()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'guest' CHECK(role IN ('guest', 'admin')),
            profile_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            rating REAL DEFAULT 4.5,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            room_number TEXT NOT NULL,
            room_type TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            price_per_night REAL NOT NULL,
            description TEXT,
            amenities TEXT,
            images TEXT,
            status TEXT DEFAULT 'available' CHECK(status IN ('available', 'booked', 'maintenance')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id),
            UNIQUE(hotel_id, room_number)
        );
        
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            hotel_id INTEGER NOT NULL,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            number_of_guests INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'confirmed' CHECK(status IN ('pending', 'confirmed', 'cancelled', 'completed')),
            special_requests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
        );
        
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            hotel_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id);
        CREATE INDEX IF NOT EXISTS idx_bookings_room ON bookings(room_id);
        CREATE INDEX IF NOT EXISTS idx_bookings_dates ON bookings(check_in_date, check_out_date);
        CREATE INDEX IF NOT EXISTS idx_rooms_hotel ON rooms(hotel_id);
        CREATE INDEX IF NOT EXISTS idx_reviews_room ON reviews(room_id);
    ''')
    conn.commit()
    conn.close()

# Helper functions
def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def generate_booking_id():
    """Generate unique booking ID"""
    return f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{secrets.token_hex(3).upper()}"

def calculate_nights(check_in, check_out):
    """Calculate number of nights"""
    check_in_dt = datetime.strptime(check_in, '%Y-%m-%d')
    check_out_dt = datetime.strptime(check_out, '%Y-%m-%d')
    return (check_out_dt - check_in_dt).days

def check_room_availability(room_id, check_in, check_out, exclude_booking_id=None):
    """Check if room is available for given dates"""
    conn = get_db_connection()
    
    query = '''
        SELECT COUNT(*) as count FROM bookings 
        WHERE room_id = ? 
        AND status IN ('confirmed', 'pending')
        AND (
            (check_in_date < ? AND check_out_date > ?)
        )
    '''
    params = [room_id, check_out, check_in]
    
    if exclude_booking_id:
        query += ' AND booking_id != ?'
        params.append(exclude_booking_id)
    
    result = conn.execute(query, params).fetchone()
    conn.close()
    
    return result['count'] == 0

# Routes
@app.route('/')
def index():
    """Home page with featured hotels"""
    conn = get_db_connection()
    featured_rooms = conn.execute('''
        SELECT r.*, h.name as hotel_name, h.city, h.rating
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
        WHERE r.status = 'available'
        LIMIT 6
    ''').fetchall()
    conn.close()
    
    return render_template('index.html', featured_rooms=featured_rooms)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()
        
        # Validation
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        if '@' not in email:
            return jsonify({'success': False, 'message': 'Invalid email address'}), 400
        
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (name, email, password, phone, role) VALUES (?, ?, ?, ?, ?)',
                (name, email, generate_password_hash(password), phone, 'guest')
            )
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'role': user['role']
            })
        
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    bookings_count = conn.execute('SELECT COUNT(*) as count FROM bookings WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user, bookings_count=bookings_count['count'])

@app.route('/search')
def search():
    """Search hotels and rooms"""
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    city = request.args.get('city', '').strip()
    room_type = request.args.get('room_type', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 10000, type=float)
    guests = request.args.get('guests', 1, type=int)
    
    conn = get_db_connection()
    
    query = '''
        SELECT r.*, h.name as hotel_name, h.city, h.rating, h.id as hotel_id
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
        WHERE r.status = 'available'
        AND r.price_per_night BETWEEN ? AND ?
        AND r.capacity >= ?
    '''
    params = [min_price, max_price, guests]
    
    if city:
        query += ' AND h.city LIKE ?'
        params.append(f'%{city}%')
    
    if room_type:
        query += ' AND r.room_type = ?'
        params.append(room_type)
    
    rooms = conn.execute(query, params).fetchall()
    
    # Filter by date availability if provided
    if check_in and check_out:
        available_rooms = []
        for room in rooms:
            if check_room_availability(room['id'], check_in, check_out):
                available_rooms.append(room)
        rooms = available_rooms
    
    conn.close()
    
    return render_template('search_results.html', 
                         rooms=rooms,
                         check_in=check_in,
                         check_out=check_out,
                         city=city,
                         room_type=room_type)

@app.route('/hotel/<int:hotel_id>')
def hotel_detail(hotel_id):
    """Hotel detail page"""
    conn = get_db_connection()
    hotel = conn.execute('SELECT * FROM hotels WHERE id = ?', (hotel_id,)).fetchone()
    
    if not hotel:
        conn.close()
        return render_template('404.html'), 404
    
    rooms = conn.execute('SELECT * FROM rooms WHERE hotel_id = ? AND status = "available"', (hotel_id,)).fetchall()
    reviews = conn.execute('''
        SELECT r.*, u.name as user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.hotel_id = ?
        ORDER BY r.created_at DESC
        LIMIT 10
    ''', (hotel_id,)).fetchall()
    
    conn.close()
    
    return render_template('hotel_detail.html', hotel=hotel, rooms=rooms, reviews=reviews)

@app.route('/room/<int:room_id>')
def room_detail(room_id):
    """Room detail page"""
    conn = get_db_connection()
    room = conn.execute('''
        SELECT r.*, h.name as hotel_name, h.city, h.rating, h.id as hotel_id
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
        WHERE r.id = ?
    ''', (room_id,)).fetchone()
    
    if not room:
        conn.close()
        return render_template('404.html'), 404
    
    reviews = conn.execute('''
        SELECT r.*, u.name as user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.room_id = ?
        ORDER BY r.created_at DESC
    ''', (room_id,)).fetchall()
    
    conn.close()
    
    return render_template('room_detail.html', room=room, reviews=reviews)

@app.route('/booking/<int:room_id>', methods=['GET', 'POST'])
@login_required
def create_booking(room_id):
    """Create booking for a room"""
    if request.method == 'POST':
        data = request.get_json()
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        guests = data.get('number_of_guests', 1)
        special_requests = data.get('special_requests', '')
        
        # Validate dates
        try:
            check_in_dt = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_dt = datetime.strptime(check_out, '%Y-%m-%d')
            
            if check_in_dt >= check_out_dt:
                return jsonify({'success': False, 'message': 'Check-out must be after check-in'}), 400
            
            if check_in_dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                return jsonify({'success': False, 'message': 'Check-in date cannot be in the past'}), 400
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format'}), 400
        
        # Check room availability
        if not check_room_availability(room_id, check_in, check_out):
            return jsonify({'success': False, 'message': 'Room not available for selected dates'}), 400
        
        conn = get_db_connection()
        room = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
        
        if not room:
            conn.close()
            return jsonify({'success': False, 'message': 'Room not found'}), 404
        
        nights = calculate_nights(check_in, check_out)
        total_price = nights * room['price_per_night']
        booking_id = generate_booking_id()
        
        try:
            conn.execute('''
                INSERT INTO bookings 
                (booking_id, user_id, room_id, hotel_id, check_in_date, check_out_date, 
                 number_of_guests, total_price, status, special_requests)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (booking_id, session['user_id'], room_id, room['hotel_id'], check_in, check_out,
                  guests, total_price, 'confirmed', special_requests))
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': 'Booking confirmed!',
                'booking_id': booking_id,
                'total_price': total_price
            })
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': f'Booking error: {str(e)}'}), 400
    
    conn = get_db_connection()
    room = conn.execute('''
        SELECT r.*, h.name as hotel_name, h.city
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
        WHERE r.id = ?
    ''', (room_id,)).fetchone()
    conn.close()
    
    if not room:
        return render_template('404.html'), 404
    
    return render_template('booking.html', room=room)

@app.route('/my-bookings')
@login_required
def my_bookings():
    """View user bookings"""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, r.room_number, r.room_type, r.price_per_night, h.name as hotel_name
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN hotels h ON b.hotel_id = h.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/booking/<booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel booking"""
    conn = get_db_connection()
    booking = conn.execute(
        'SELECT * FROM bookings WHERE booking_id = ? AND user_id = ?',
        (booking_id, session['user_id'])
    ).fetchone()
    
    if not booking:
        conn.close()
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    if booking['status'] == 'cancelled':
        conn.close()
        return jsonify({'success': False, 'message': 'Booking already cancelled'}), 400
    
    try:
        conn.execute(
            'UPDATE bookings SET status = ? WHERE booking_id = ?',
            ('cancelled', booking_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Booking cancelled successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db_connection()
    
    stats = {
        'total_hotels': conn.execute('SELECT COUNT(*) as count FROM hotels').fetchone()['count'],
        'total_rooms': conn.execute('SELECT COUNT(*) as count FROM rooms').fetchone()['count'],
        'total_bookings': conn.execute('SELECT COUNT(*) as count FROM bookings').fetchone()['count'],
        'total_users': conn.execute('SELECT COUNT(*) as count FROM users WHERE role = "guest"').fetchone()['count'],
        'total_revenue': conn.execute('SELECT SUM(total_price) as sum FROM bookings WHERE status = "confirmed"').fetchone()['sum'] or 0,
        'pending_bookings': conn.execute('SELECT COUNT(*) as count FROM bookings WHERE status = "pending"').fetchone()['count'],
    }
    
    recent_bookings = conn.execute('''
        SELECT b.*, r.room_number, h.name as hotel_name, u.name as user_name
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN hotels h ON b.hotel_id = h.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', stats=stats, recent_bookings=recent_bookings)

@app.route('/admin/hotels')
@admin_required
def admin_hotels():
    """Manage hotels"""
    conn = get_db_connection()
    hotels = conn.execute('SELECT * FROM hotels').fetchall()
    conn.close()
    
    return render_template('admin_hotels.html', hotels=hotels)

@app.route('/admin/hotels/add', methods=['POST'])
@admin_required
def add_hotel():
    """Add hotel"""
    data = request.get_json()
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO hotels (name, description, city, address, phone, email, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data.get('description', ''), data['city'], data['address'],
              data.get('phone', ''), data.get('email', ''), data.get('rating', 4.5)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Hotel added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/rooms')
@admin_required
def admin_rooms():
    """Manage rooms"""
    conn = get_db_connection()
    rooms = conn.execute('''
        SELECT r.*, h.name as hotel_name
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
    ''').fetchall()
    
    hotels = conn.execute('SELECT * FROM hotels').fetchall()
    conn.close()
    
    return render_template('admin_rooms.html', rooms=rooms, hotels=hotels)

@app.route('/admin/rooms/add', methods=['POST'])
@admin_required
def add_room():
    """Add room"""
    data = request.get_json()
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO rooms 
            (hotel_id, room_number, room_type, capacity, price_per_night, description, amenities, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['hotel_id'], data['room_number'], data['room_type'], data['capacity'],
              data['price_per_night'], data.get('description', ''), data.get('amenities', ''), 'available'))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Room added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    """Manage bookings"""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, r.room_number, h.name as hotel_name, u.name as user_name
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN hotels h ON b.hotel_id = h.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/api/check-availability', methods=['POST'])
def check_availability_api():
    """API to check room availability"""
    data = request.get_json()
    room_id = data.get('room_id')
    check_in = data.get('check_in_date')
    check_out = data.get('check_out_date')
    
    available = check_room_availability(room_id, check_in, check_out)
    
    return jsonify({'available': available})

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
