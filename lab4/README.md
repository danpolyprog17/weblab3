# User Management System

A Flask-based web application for managing user accounts with authentication and role-based access control.

## Features

- User authentication (login/logout)
- User management (create, read, update, delete)
- Role-based access control
- Password change functionality
- Form validation
- Responsive Bootstrap UI

## Requirements

- Python 3.8+
- Flask and other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
```bash
python run.py
```
3. Open your browser and navigate to `http://localhost:5000`

## Testing

Run the tests using pytest:
```bash
pytest
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── auth.py
│   │   └── users.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       │   ├── login.html
│       │   └── change_password.html
│       └── users/
│           ├── form.html
│           └── view.html
├── requirements.txt
├── run.py
└── README.md
```

## Security Notes

- The application uses Flask-Login for authentication
- Passwords are hashed using Werkzeug's security functions
- Form validation is implemented both client-side and server-side
- CSRF protection is enabled by default

## License

This project is licensed under the MIT License. 