# 🧭 TourApp API

A RESTful API for managing travel locations and user bookings, built with Django REST Framework. Includes secure user authentication (JWT), password reset via email, and admin-managed locations.

---

## 🚀 Features

### 🔐 Authentication & Security
- User Signup with email, full name, and password
- JWT-based login with user details in response
- Password reset via email with token + link verification
- Custom user model with `email` as the login field

### 🌍 Location Management
- Admins can create/update/delete locations
- Authenticated users can view/search all locations
- Location data includes name, description, images, location URL

### 📆 Booking System
- Authenticated users can book a location with a date
- Bookings are linked to both user and location
- Users can view and delete their own bookings

---

## 🛠️ Tech Stack

- Python 3.13  
- Django 5.2  
- Django REST Framework  
- SimpleJWT for authentication  
- SQLite  

---
