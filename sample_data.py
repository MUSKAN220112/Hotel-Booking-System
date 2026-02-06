"""
Sample Data Initialization Script
Populates the database with demo data for testing
Made by Muskan
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DATABASE = 'hotel_booking.db'

def init_sample_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    try:
        # Add sample users
        users = [
            ('Admin User', 'admin@hotel.com', generate_password_hash('admin123'), '+1-800-STAY-NOW', 'admin'),
            ('Muskan', 'muskan@smartstay.com', generate_password_hash('muskan123'), '+1-555-0100', 'admin'),
            ('John Doe', 'john@example.com', generate_password_hash('password123'), '+1-555-0101', 'guest'),
            ('Jane Smith', 'jane@example.com', generate_password_hash('password123'), '+1-555-0102', 'guest'),
            ('Mike Johnson', 'mike@example.com', generate_password_hash('password123'), '+1-555-0103', 'guest'),
        ]
        
        for user in users:
            c.execute(
                'INSERT INTO users (name, email, password, phone, role) VALUES (?, ?, ?, ?, ?)',
                user
            )
        
        # Add sample hotels
        hotels = [
            ('Grand Plaza Hotel', 'A luxurious 5-star hotel in the heart of the city', 'New York', '123 Main St, NYC', '+1-212-555-0100', 'info@grandplaza.com', 4.8),
            ('Ocean View Resort', 'Beautiful beachfront resort with stunning ocean views', 'Miami', '456 Beach Ave, Miami', '+1-305-555-0200', 'info@oceanview.com', 4.7),
            ('Mountain Lodge', 'Cozy mountain retreat perfect for nature lovers', 'Denver', '789 Peak Rd, Denver', '+1-303-555-0300', 'info@mountainlodge.com', 4.6),
            ('Urban boutique Hotel', 'Modern boutique hotel in downtown LA', 'Los Angeles', '321 Hollywood Blvd, LA', '+1-213-555-0400', 'info@urbanboutique.com', 4.5),
            ('Historic Inn', 'Charming historic hotel with classic elegance', 'Boston', '654 Heritage St, Boston', '+1-617-555-0500', 'info@historicinn.com', 4.9),
        ]
        
        hotel_ids = []
        for hotel in hotels:
            c.execute(
                'INSERT INTO hotels (name, description, city, address, phone, email, rating) VALUES (?, ?, ?, ?, ?, ?, ?)',
                hotel
            )
            hotel_ids.append(c.lastrowid)
        
        # Add sample rooms
        rooms = [
            # Grand Plaza Hotel rooms
            (hotel_ids[0], '101', 'Single', 1, 99.00, 'Cozy single room with city view', 'WiFi, AC, TV, Work Desk'),
            (hotel_ids[0], '102', 'Double', 2, 149.00, 'Comfortable double room with queen bed', 'WiFi, AC, TV, Mini-bar, Bathrobe'),
            (hotel_ids[0], '201', 'Suite', 4, 299.00, 'Luxurious suite with living area', 'WiFi, AC, TV, Mini-bar, Jacuzzi, City View'),
            
            # Ocean View Resort rooms
            (hotel_ids[1], '201', 'Single', 1, 89.00, 'Single room with balcony', 'WiFi, AC, TV, Beach Access'),
            (hotel_ids[1], '202', 'Double', 2, 139.00, 'Double room with ocean view', 'WiFi, AC, TV, Balcony, Beach Access'),
            (hotel_ids[1], '301', 'Penthouse', 6, 399.00, 'Exclusive penthouse with panoramic views', 'WiFi, AC, TV, Infinity Pool, Private Beach'),
            
            # Mountain Lodge rooms
            (hotel_ids[2], '101', 'Single', 1, 79.00, 'Cozy cabin style room', 'WiFi, Fireplace, TV, Mountain View'),
            (hotel_ids[2], '102', 'Double', 2, 129.00, 'Rustic double room with fireplace', 'WiFi, Fireplace, TV, Balcony'),
            
            # Urban Boutique Hotel rooms
            (hotel_ids[3], '501', 'Suite', 2, 259.00, 'Modern suite with city skyline view', 'WiFi, AC, TV, Mini-bar, Work Area'),
            
            # Historic Inn rooms
            (hotel_ids[4], '101', 'Double', 2, 169.00, 'Historic room with period furniture', 'WiFi, AC, TV, Antique Decor'),
            (hotel_ids[4], '102', 'Suite', 3, 329.00, 'Grand suite with elegant décor', 'WiFi, AC, TV, Parlor, Fireplace'),
        ]
        
        room_ids = []
        for room in rooms:
            c.execute(
                'INSERT INTO rooms (hotel_id, room_number, room_type, capacity, price_per_night, description, amenities, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                room + ('available',)
            )
            room_ids.append(c.lastrowid)
        
        # Add sample bookings
        today = datetime.now()
        bookings = [
            (3, room_ids[1], (today + timedelta(days=5)).date(), (today + timedelta(days=7)).date(), 2, 298.00, 'confirmed', 'Non-smoking room preferred'),
            (4, room_ids[4], (today + timedelta(days=10)).date(), (today + timedelta(days=12)).date(), 2, 278.00, 'confirmed', ''),
            (5, room_ids[8], (today + timedelta(days=15)).date(), (today + timedelta(days=17)).date(), 1, 259.00, 'pending', 'High floor requested'),
        ]
        
        for i, booking in enumerate(bookings):
            booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{str(i).zfill(3)}"
            c.execute(
                'INSERT INTO bookings (booking_id, user_id, room_id, hotel_id, check_in_date, check_out_date, number_of_guests, total_price, status, special_requests) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (booking_id, booking[0], booking[1], hotels.index([h for h in hotels if h[0] in ['Grand Plaza Hotel']][0]) + 1, booking[2], booking[3], booking[4], booking[5], booking[6], booking[7])
            )
        
        # Add sample reviews
        reviews = [
            (3, room_ids[1], hotel_ids[0], 5, 'Excellent service and beautiful room! Highly recommended.', 'Amazing Experience'),
            (4, room_ids[4], hotel_ids[1], 4, 'Great beach access and friendly staff.', 'Good Value'),
            (5, room_ids[8], hotel_ids[3], 5, 'Modern amenities and perfect location.', 'Perfect Stay'),
        ]
        
        for review in reviews:
            c.execute(
                'INSERT INTO reviews (user_id, room_id, hotel_id, rating, comment, title) VALUES (?, ?, ?, ?, ?, ?)',
                review
            )
        
        conn.commit()
        print("✅ Sample data initialized successfully!")
        print(f"   - 5 Users created")
        print(f"   - 5 Hotels created")
        print(f"   - 11 Rooms created")
        print(f"   - 3 Bookings created")
        print(f"   - 3 Reviews created")
        
    except sqlite3.IntegrityError as e:
        print(f"⚠️  Data already exists: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_sample_data()
