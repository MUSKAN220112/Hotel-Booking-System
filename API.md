# SmartStay Hotel Booking System - API Documentation

**Made by: Muskan Chohan**

---

## Base URL

```
Local Development: http://localhost:5000
Production: https://hotel-booking-system.render.com
```

---

## Authentication

Most endpoints require user authentication via Flask session.

### Session-Based Authentication

1. **Register:** Create a new account
2. **Login:** Obtain session cookie
3. **Access Protected Routes:** Use session cookie for subsequent requests
4. **Logout:** Clear session

---

## API Endpoints

### 1. Authentication Endpoints

#### Register New User

```http
POST /register
Content-Type: application/x-www-form-urlencoded

name=John Doe&email=john@example.com&password=Pass123!&confirm_password=Pass123!
```

**Response (Success - 302 Redirect):**
```
Location: /login
Flash Message: "Account created successfully! Please login."
```

**Response (Error - 400):**
```
Flash Message: "Email already registered!"
```

**Validation Rules:**
- Name: Minimum 3 characters
- Email: Valid email format, must be unique
- Password: Minimum 8 characters
- Passwords must match

---

#### Login User

```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=Pass123!
```

**Response (Success - 302 Redirect):**
```
Location: /
Flash Message: "Login successful!"
Session: user_id, user_email
```

**Response (Error - 401):**
```
Flash Message: "Invalid email or password!"
```

---

#### Logout

```http
GET /logout
```

**Response (302 Redirect):**
```
Location: /
Session: Cleared
```

---

### 2. Hotel & Room Endpoints

#### Search Hotels & Rooms

```http
GET /search
Query Parameters:
- city (optional): City name
- check_in (optional): YYYY-MM-DD
- check_out (optional): YYYY-MM-DD
- room_type (optional): single, double, suite, penthouse
- min_price (optional): Minimum price
- max_price (optional): Maximum price
```

**Example:**
```
GET /search?city=Mumbai&check_in=2026-02-10&check_out=2026-02-12&min_price=2000&max_price=10000
```

**Response (200 OK):**
```json
{
    "hotels": [
        {
            "id": 1,
            "name": "Grand Plaza Hotel",
            "city": "Mumbai",
            "rating": 4.5,
            "rooms": [
                {
                    "id": 1,
                    "room_number": "101",
                    "room_type": "Double",
                    "capacity": 2,
                    "price_per_night": 5000,
                    "amenities": ["WiFi", "AC", "TV"],
                    "available": true
                }
            ]
        }
    ],
    "total_results": 5
}
```

---

#### Get Hotel Details

```http
GET /hotel/<hotel_id>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Grand Plaza Hotel",
    "description": "Luxury 5-star hotel...",
    "city": "Mumbai",
    "address": "123 Main Street, Mumbai",
    "phone": "+91-9876543210",
    "email": "info@grandplaza.com",
    "rating": 4.5,
    "rooms": [
        {
            "id": 1,
            "room_type": "Double",
            "capacity": 2,
            "price_per_night": 5000
        }
    ],
    "reviews": [
        {
            "user_name": "John Doe",
            "rating": 5,
            "title": "Excellent stay!",
            "comment": "Great service and clean rooms..."
        }
    ]
}
```

---

#### Get Room Details

```http
GET /room/<room_id>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "hotel_id": 1,
    "hotel_name": "Grand Plaza Hotel",
    "room_number": "101",
    "room_type": "Double",
    "capacity": 2,
    "price_per_night": 5000,
    "description": "Spacious double room with...",
    "amenities": [
        "WiFi",
        "Air Conditioning",
        "Smart TV",
        "Mini Bar",
        "Bathroom with bathtub"
    ],
    "images": [
        "/static/images/room1.jpg",
        "/static/images/room2.jpg"
    ],
    "reviews": [
        {
            "user_name": "John Doe",
            "rating": 5,
            "title": "Perfect room!",
            "comment": "Clean, comfortable, and beautiful view"
        }
    ]
}
```

---

### 3. Booking Endpoints

#### Create Booking

```http
POST /booking/<room_id>
Content-Type: application/x-www-form-urlencoded

check_in=2026-02-10&check_out=2026-02-12&guests=2&special_requests=Early+checkout
```

**Request Headers:**
```
Cookie: session=<session_cookie>
```

**Response (Success - 302 Redirect):**
```
Location: /my-bookings
Flash Message: "Booking confirmed! Booking ID: BK20260210ABC123"
Session: booking_id stored
```

**Response (Error):**

*Room not available:*
```
Status: 409 Conflict
Flash Message: "Room not available for selected dates!"
```

*Invalid dates:*
```
Status: 400 Bad Request
Flash Message: "Check-out date must be after check-in date!"
```

**Validation Rules:**
- Check-in date >= today
- Check-out date > check-in date
- Room must be available (no overlapping bookings)
- Guest count <= room capacity

---

#### Get Booking Details

```http
GET /booking/<booking_id>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "booking_id": "BK20260210ABC123",
    "user_email": "john@example.com",
    "hotel_name": "Grand Plaza Hotel",
    "room_number": "101",
    "check_in": "2026-02-10",
    "check_out": "2026-02-12",
    "number_of_guests": 2,
    "total_nights": 2,
    "price_per_night": 5000,
    "total_price": 10000,
    "status": "confirmed",
    "special_requests": "Early checkout",
    "created_at": "2026-02-06T10:30:00"
}
```

---

#### List User Bookings

```http
GET /my-bookings
```

**Response (200 OK):**
```json
{
    "bookings": [
        {
            "booking_id": "BK20260210ABC123",
            "hotel_name": "Grand Plaza Hotel",
            "room_number": "101",
            "check_in": "2026-02-10",
            "check_out": "2026-02-12",
            "total_price": 10000,
            "status": "confirmed",
            "created_at": "2026-02-06"
        }
    ],
    "total_bookings": 5,
    "total_spent": 50000
}
```

---

#### Cancel Booking

```http
POST /booking/<booking_id>/cancel
```

**Response (Success):**
```
Status: 200 OK
Flash Message: "Booking cancelled successfully!"
JSON Response: {"status": "cancelled", "refund": 10000}
```

**Response (Error):**

*Booking not found:*
```
Status: 404 Not Found
Message: "Booking not found!"
```

*Cannot cancel:*
```
Status: 400 Bad Request
Message: "Booking cannot be cancelled!"
```

---

### 4. User Profile Endpoints

#### Get User Profile

```http
GET /profile
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "role": "guest",
    "member_since": "2026-01-15",
    "total_bookings": 5,
    "total_spent": 50000,
    "average_rating": 4.2
}
```

---

#### Update User Profile

```http
POST /profile
Content-Type: application/x-www-form-urlencoded

name=John Doe&phone=9876543210
```

**Response (Success):**
```
Status: 200 OK
Flash Message: "Profile updated successfully!"
```

---

### 5. Admin Endpoints

**Requires Admin Authentication** (@admin_required)

#### Admin Dashboard

```http
GET /admin
```

**Response (200 OK):**
```json
{
    "total_bookings": 150,
    "total_revenue": 7500000,
    "bookings_this_week": 25,
    "occupancy_rate": 85.5,
    "recent_bookings": [
        {
            "booking_id": "BK20260206ABC123",
            "hotel_name": "Grand Plaza Hotel",
            "guest_name": "John Doe",
            "check_in": "2026-02-10",
            "total_price": 10000,
            "status": "confirmed"
        }
    ]
}
```

---

#### Add Hotel

```http
POST /admin/hotels/add
Content-Type: application/x-www-form-urlencoded

name=New Hotel&city=Delhi&address=123 Street&phone=9876543210&email=hotel@example.com&description=Beautiful hotel...
```

**Response (Success):**
```
Status: 201 Created
Flash Message: "Hotel added successfully!"
JSON: {"hotel_id": 10, "name": "New Hotel"}
```

---

#### Add Room

```http
POST /admin/rooms/add
Content-Type: application/x-www-form-urlencoded

hotel_id=1&room_number=102&room_type=Double&capacity=2&price_per_night=5000&amenities=WiFi,AC,TV
```

**Response (Success):**
```
Status: 201 Created
Flash Message: "Room added successfully!"
JSON: {"room_id": 50, "room_number": "102"}
```

---

#### List All Bookings (Admin)

```http
GET /admin/bookings
```

**Response (200 OK):**
```json
{
    "bookings": [
        {
            "booking_id": "BK20260210ABC123",
            "guest_email": "john@example.com",
            "hotel_name": "Grand Plaza Hotel",
            "check_in": "2026-02-10",
            "check_out": "2026-02-12",
            "total_price": 10000,
            "status": "confirmed"
        }
    ],
    "total": 150,
    "status_breakdown": {
        "confirmed": 120,
        "pending": 20,
        "cancelled": 10
    }
}
```

---

### 6. AJAX API Endpoints

#### Check Room Availability

```http
POST /api/check-availability
Content-Type: application/json

{
    "room_id": 1,
    "check_in": "2026-02-10",
    "check_out": "2026-02-12"
}
```

**Response (Available):**
```json
{
    "available": true,
    "message": "Room is available for selected dates",
    "price_per_night": 5000,
    "total_nights": 2,
    "total_price": 10000
}
```

**Response (Not Available):**
```json
{
    "available": false,
    "message": "Room is not available for selected dates"
}
```

---

#### Health Check

```http
GET /api/health
```

**Response (200 OK):**
```json
{
    "status": "healthy",
    "database": "connected",
    "version": "1.0.0",
    "timestamp": "2026-02-06T10:30:00",
    "uptime_seconds": 3600
}
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 302 | Redirect - Redirect to another page |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Not authenticated |
| 403 | Forbidden - Not authorized |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Room not available |
| 500 | Server Error - Internal error |

---

## Error Handling

All error responses include:

```json
{
    "status": "error",
    "message": "Descriptive error message",
    "code": "ERROR_CODE"
}
```

**Common Error Codes:**
- `INVALID_INPUT`: Input validation failed
- `ROOM_UNAVAILABLE`: Room not available for dates
- `UNAUTHORIZED`: Not authenticated
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Booking conflict
- `DATABASE_ERROR`: Database operation failed

---

## Rate Limiting

No explicit rate limiting implemented. For production, consider:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: session.get('user_id'))

@app.route('/api/check-availability', methods=['POST'])
@limiter.limit("100 per hour")
def check_availability():
    # ...
```

---

## CORS Headers

For development:
```
Access-Control-Allow-Origin: *
```

For production, configure specific origins:
```python
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://yourdomain.com'
    return response
```

---

## Request/Response Examples

### Example: Complete Booking Flow

#### 1. Search

```bash
curl "http://localhost:5000/search?city=Mumbai&check_in=2026-02-10&check_out=2026-02-12"
```

#### 2. Get Room Details

```bash
curl "http://localhost:5000/room/1"
```

#### 3. Check Availability

```bash
curl -X POST "http://localhost:5000/api/check-availability" \
  -H "Content-Type: application/json" \
  -d '{"room_id":1,"check_in":"2026-02-10","check_out":"2026-02-12"}'
```

#### 4. Create Booking

```bash
curl -X POST "http://localhost:5000/booking/1" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "check_in=2026-02-10&check_out=2026-02-12&guests=2" \
  -c cookies.txt
```

#### 5. View Booking

```bash
curl "http://localhost:5000/my-bookings" \
  -b cookies.txt
```

---

## Testing with Postman

1. Import collection from `/postman/collection.json`
2. Set environment variables:
   - `base_url`: http://localhost:5000
   - `admin_email`: admin@hotel.com
   - `admin_password`: admin123

3. Run requests in sequence for complete flow testing

---

## WebSocket Support (Future)

For real-time availability updates:

```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('check-availability')
def handle_availability(data):
    available = check_room_availability(data)
    emit('availability', available)
```

---

## Webhooks (Future)

Notify external services on booking events:

```python
import requests

def trigger_webhook(event, data):
    requests.post(
        os.getenv('WEBHOOK_URL'),
        json={'event': event, 'data': data}
    )
```

---

## GraphQL API (Future)

Consider implementing GraphQL for flexible queries:

```graphql
query {
  hotels {
    id
    name
    rooms(available: true) {
      id
      pricePerNight
    }
  }
}
```

---

## API Versioning

Current version: v1.0.0

For future versions:
```
/api/v2/hotels
/api/v2/bookings
```

---

## Documentation Tools

Generate OpenAPI/Swagger docs:

```python
from flasgger import Swagger

swagger = Swagger(app)
```

Access at: `http://localhost:5000/apidocs`

---

**Last Updated:** February 2026

**Made by: Muskan**
