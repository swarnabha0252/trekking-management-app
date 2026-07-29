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
- Admin dashboard layout
- Responsive sidebar navigation
- Dashboard statistics cards (UI)
- Account approval check
- User blacklist check
- Password visibility toggle
- Responsive interface using Bootstrap 5
- Jinja2 templating

### Planned

- Trek management
- Staff management
- User management
- Booking management
- Trek Staff dashboard
- User dashboard
- Recent bookings section
- Reports and analytics
- Search functionality
- Settings page

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
├── extensions.py
├── models/
│   └── user.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── staff_dashboard.html
│   └── user_dashboard.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── instance/
├── requirements.txt
├── .gitignore
└── README.md
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

```
http://127.0.0.1:5000/login
```

---

## Screens Implemented

- Login Page
- Registration Page
- Admin Dashboard (UI)

---

## Future Enhancements

- Complete Admin Dashboard
- Trek CRUD Operations
- Staff Approval System
- User Management
- Booking Management
- Reports & Analytics
- Search & Filtering
- Responsive Dashboard Improvements

---

## License

This project is developed for academic purposes as part of the **Modern Application Development - I** course in the **IIT Madras BS Degree Program**.