# Flask Web Application

This is a Flask web application that demonstrates various features including:
- URL parameters handling
- Request headers display
- Cookie management
- Form parameters processing
- Phone number validation

## Features

1. **URL Parameters Page**
   - Displays all parameters passed in the URL
   - Example: `/url_params?param1=value1&param2=value2`

2. **Headers Page**
   - Shows all request headers
   - Displays header names and values

3. **Cookies Page**
   - Displays all cookies
   - Manages a special cookie (sets if not present, deletes if present)

4. **Form Parameters Page**
   - Simple form with name and email fields
   - Displays submitted form data

5. **Phone Validation Page**
   - Validates phone numbers in various formats
   - Supports formats like:
     - +7 (123) 456-75-90
     - 8(123)4567590
     - 123.456.75.90
   - Formats valid numbers to 8-***-***-**-**
   - Shows appropriate error messages for invalid input

## Setup and Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Running Tests

To run the test suite:
```bash
pytest
```

## Requirements

- Python 3.7+
- Flask 3.0.2
- pytest 8.0.2
- pytest-flask 1.3.0 