# trekking-management-app

A web application for managing trekking activities, developed using Flask.

This project is being developed as part of the Modern Application Development - I course in the IIT Madras BS Degree program.

## Features

### Current

- User registration
- User login
- Secure password hashing
- Session management
- Logout functionality
- Role management
- Account approval check
- User blacklist check
- Password visibility toggle
- Responsive interface using Bootstrap 5
- Jinja template inheritance

### Planned

- Role-based access control
- Admin dashboard
- Trek Staff dashboard
- User dashboard
- Trek management
- Booking management

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Jinja2
- Bootstrap 5
- HTML
- CSS
- JavaScript
- SQLite

## Project Structure

```text
trekking-management-app/
├── app.py
├── extensions.py
├── models/
│   └── user.py
├── templates/
├── static/
├── instance/
├── requirements.txt
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/swarnabha0252/trekking-management-app.git
```

### Move to the project directory

```bash
cd trekking-management-app
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

```bash
.venv\Scripts\activate
```

### Install the required packages

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

### Open the application at

```
http://127.0.0.1:5000/login
```

## License

This project is developed for academic purposes.