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
- Admin dashboard
- Manage treks
- Add trek
- Edit trek
- Delete trek
- Assign trek staff
- Reassign trek staff
- Manage staff
- Approve staff accounts
- Reject staff accounts
- Automatic trek opening after staff assignment
- Manual booking open/close by admin
- Automatic booking closure when all slots are filled
- User dashboard
- View available treks
- Trek booking
- Duplicate booking prevention
- View booking details
- Cancel booking
- Automatic slot restoration after cancellation
- My Bookings
- Responsive interface using Bootstrap 5
- Jinja2 templating

### Planned

- Trek Staff dashboard
- Participant management
- Trek completion workflow
- Booking completion workflow
- Reports and analytics
- Search functionality
- Settings page
- Profile management
- Dashboard improvements

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
    ├── manage_staff.html
    ├── manage_treks.html
    ├── manage_users.html
    ├── my_bookings.html
    ├── register.html
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

## Screens Implemented

- Login Page
- Registration Page
- Admin Dashboard
- Manage Treks
- Manage Staff
- Manage Users
- User Dashboard
- My Bookings

---

## Future Enhancements

- Complete Trek Staff Dashboard
- Participant Management
- Trek Completion Workflow
- Booking Completion Workflow
- Reports & Analytics
- Search & Filtering
- Profile Management
- Dashboard Improvements
- AJAX-based Notifications

---

## License

This project is developed for academic purposes as part of the **Modern Application Development - I** course in the **IIT Madras BS Degree Program**.