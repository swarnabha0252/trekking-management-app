# Trekking Management App

A web application for managing trekking activities, developed using Flask.

This project is being developed as part of the **Modern Application Development - I** course in the **IIT Madras BS Degree Program**.

---

## Features

### Current

- User registration
- User login
- Secure password hashing
- Session management
- Logout functionality
- Role-based access control (Admin, Trek Staff, User)
- Template inheritance using Jinja2 (`base.html`)
- Responsive interface using Bootstrap 5

### Admin

- Admin dashboard
- Dashboard statistics
- Manage treks
- Add trek
- Edit trek
- Delete trek
- Assign trek staff
- Reassign trek staff
- View assigned staff profile
- Manage staff
- Approve staff accounts
- Reject staff accounts
- Manage users
- Manage bookings
- View booking details
- Cancel bookings
- Search users, trek staff, treks, and bookings
- Reports dashboard
- Revenue analytics
- Booking statistics
- Most popular trek analytics
- Most active user analytics
- Most active trek staff analytics
- Automatic trek opening after staff assignment
- Manual booking open/close
- Automatic booking closure when all slots are filled
- Read-only completed treks
- Permanent booking closure after trek completion

### User

- User dashboard
- View available treks
- View trek details
- Trek booking
- Duplicate booking prevention
- View booking details
- Cancel booking
- Automatic slot restoration after cancellation
- My Bookings page
- Profile management
- Edit profile details
- Add phone number

### Trek Staff

- Staff dashboard
- View assigned treks
- View trek details
- View trek participants
- Mark trek as completed
- Automatic booking completion after trek completion

### Planned

- Settings page
- Dashboard improvements
- AJAX-based notifications
- Email notifications
- Pagination for large datasets
- Export reports as PDF/CSV

---

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

---

## Project Structure

```text
trekking-management-app/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── README.md
├── .gitignore
├── instance/
│   └── trekking.db
├── models/
│   ├── booking.py
│   ├── trek.py
│   └── user.py
├── routes/
│   ├── admin.py
│   ├── auth.py
│   ├── staff.py
│   └── user.py
├── static/
│   └── style.css
└── templates/
    ├── admin_dashboard.html
    ├── base.html
    ├── login.html
    ├── manage_bookings.html
    ├── manage_staff.html
    ├── manage_treks.html
    ├── manage_users.html
    ├── my_bookings.html
    ├── profile.html
    ├── register.html
    ├── reports.html
    ├── search_results.html
    ├── settings.html
    ├── staff_dashboard.html
    └── user_dashboard.html
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/swarnabha0252/trekking-management-app.git
```

### 2. Move to the project directory

```bash
cd trekking-management-app
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 5. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open the application

```text
http://127.0.0.1:5000/login
```

---

## User Roles

### Admin

- Manage treks
- Manage users
- Manage trek staff
- Manage bookings
- Assign and reassign trek staff
- Open and close trek bookings
- View reports and analytics
- Search across the system

### Trek Staff

- View assigned treks
- View participants
- Mark assigned treks as completed

### User

- Browse available treks
- Book treks
- View booking history
- Cancel active bookings

---

## Business Rules

- Only approved trek staff can be assigned to treks.
- A trek automatically opens after a guide is assigned.
- Bookings close automatically when all available slots are filled.
- Users cannot book the same trek more than once.
- Cancelling a booking restores one available slot.
- Completed treks become read-only.
- Completing a trek automatically marks all active bookings as completed.

---

## Screens Implemented

- Login Page
- Registration Page
- Admin Dashboard
- Manage Treks
- Manage Staff
- Manage Users
- Manage Bookings
- Reports Dashboard
- Search Results
- User Dashboard
- My Bookings
- Staff Dashboard

---

## Future Enhancements

- Profile Management
- Settings Page
- Email Notifications
- AJAX-based Notifications
- Pagination
- Advanced Filters
- Export Reports (PDF/CSV)
- Image Upload for Treks
- Trek Reviews and Ratings
- Payment Gateway Integration

---

## License

This project is developed for academic purposes as part of the **Modern Application Development - I** course in the **IIT Madras BS Degree Program**.