# SmartStay Hotel Booking System - Database Schema

## Overview
This document outlines the complete database schema for the SmartStay Hotel Booking System.

**Made by: Muskan Chohan**

---

## Database Design

### 1. **Users Table**
Stores user account information with role-based access control.

```sql
CREATE TABLE users (
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
```

**Fields:**
- `id`: Unique user identifier
- `name`: Full name of the user
- `email`: Unique email address (primary login credential)
- `password`: Hashed password
- `phone`: Contact phone number
- `role`: User type ('guest' or 'admin')
- `profile_image`: Path to user profile picture
- `created_at`: Account creation timestamp
- `updated_at`: Last account update timestamp

---

### 2. **Hotels Table**
Contains information about hotels in the system.

```sql
CREATE TABLE hotels (
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
```

**Fields:**
- `id`: Unique hotel identifier
- `name`: Hotel name
- `description`: Detailed description
- `city`: City where hotel is located
- `address`: Full street address
- `phone`: Hotel contact number
- `email`: Hotel email address
- `rating`: Average rating (1-5 stars)
- `image`: Hotel featured image path
- `created_at`: Record creation timestamp

---

### 3. **Rooms Table**
Details about individual rooms in each hotel.

```sql
CREATE TABLE rooms (
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

-- Index for performance
CREATE INDEX idx_rooms_hotel ON rooms(hotel_id);
```

**Fields:**
- `id`: Unique room identifier
- `hotel_id`: Foreign key to hotels table
- `room_number`: Room number/identifier
- `room_type`: Type of room (Single, Double, Suite, Penthouse)
- `capacity`: Maximum number of guests
- `price_per_night`: Nightly rate
- `description`: Room description
- `amenities`: Available amenities (comma-separated)
- `images`: JSON array of image paths
- `status`: Room availability status
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp

---

### 4. **Bookings Table**
Manages all room reservations.

```sql
CREATE TABLE bookings (
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

-- Indexes for performance
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_room ON bookings(room_id);
CREATE INDEX idx_bookings_dates ON bookings(check_in_date, check_out_date);
```

**Fields:**
- `id`: Auto-increment primary key
- `booking_id`: Unique booking reference number (e.g., BK202602061234ABC)
- `user_id`: Foreign key to users table
- `room_id`: Foreign key to rooms table
- `hotel_id`: Foreign key to hotels table
- `check_in_date`: Reservation start date
- `check_out_date`: Reservation end date
- `number_of_guests`: Number of people staying
- `total_price`: Total booking amount
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `special_requests`: Any special guest requests
- `created_at`: Booking creation timestamp
- `updated_at`: Last update timestamp

---

### 5. **Reviews Table**
Guest reviews and ratings for hotels and rooms.

```sql
CREATE TABLE reviews (
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

-- Index for performance
CREATE INDEX idx_reviews_room ON reviews(room_id);
```

**Fields:**
- `id`: Unique review identifier
- `user_id`: Guest who wrote the review
- `room_id`: Room being reviewed
- `hotel_id`: Hotel being reviewed
- `rating`: Star rating (1-5)
- `comment`: Detailed review text
- `title`: Review title/summary
- `created_at`: Review creation timestamp

---

## Key Relationships

```
Hotels (1) ──────── (Many) Rooms
                       │
                       ├──── (Many) Bookings
                       └──── (Many) Reviews
                       
Users (1) ──────── (Many) Bookings
       │
       └──── (Many) Reviews
```

---

## Data Integrity Features

1. **Primary Keys**: All tables have auto-incrementing primary keys
2. **Foreign Keys**: Proper relationships with referential integrity
3. **Unique Constraints**:
   - `users.email`: Ensures unique email addresses
   - `bookings.booking_id`: Unique booking reference
   - `rooms.hotel_id, room_number`: No duplicate room numbers per hotel

4. **Check Constraints**:
   - `rooms.status`: Only valid statuses allowed
   - `bookings.status`: Only valid booking statuses
   - `reviews.rating`: Rating must be 1-5

5. **Default Values**:
   - `rooms.status`: 'available'
   - `bookings.status`: 'confirmed'
   - `users.role`: 'guest'
   - `hotels.rating`: 4.5

---

## Indexes

Indexes are created for frequently queried columns:

1. `idx_rooms_hotel`: Fast room lookups by hotel
2. `idx_bookings_user`: Quick access to user's bookings
3. `idx_bookings_room`: Find bookings for a specific room
4. `idx_bookings_dates`: Efficient date range queries
5. `idx_reviews_room`: Get reviews for a specific room

---

## Sample Queries

### Find Available Rooms
```sql
SELECT * FROM rooms 
WHERE hotel_id = ? AND status = 'available'
ORDER BY price_per_night;
```

### Check Room Availability for Dates
```sql
SELECT COUNT(*) FROM bookings 
WHERE room_id = ? 
  AND status IN ('confirmed', 'pending')
  AND (check_in_date < ? AND check_out_date > ?);
```

### Get User's Bookings
```sql
SELECT b.*, r.room_number, h.name as hotel_name 
FROM bookings b
JOIN rooms r ON b.room_id = r.id
JOIN hotels h ON b.hotel_id = h.id
WHERE b.user_id = ?
ORDER BY b.created_at DESC;
```

### Average Hotel Rating
```sql
SELECT h.id, h.name, AVG(r.rating) as avg_rating
FROM hotels h
LEFT JOIN reviews r ON h.id = r.hotel_id
GROUP BY h.id
ORDER BY avg_rating DESC;
```

---

## Database Statistics

- **Tables**: 5 (Users, Hotels, Rooms, Bookings, Reviews)
- **Indexes**: 5 (for performance optimization)
- **Relationships**: Fully normalized (3NF)
- **Constraints**: Complete data validation

---

## Notes

- All timestamps are stored in UTC
- Passwords are hashed using Werkzeug security
- Booking IDs are unique and human-readable
- The system supports soft deletes through status fields
- All financial amounts are stored as REAL (floating point)
