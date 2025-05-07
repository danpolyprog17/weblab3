from flask import Flask, render_template, request, make_response, redirect, url_for
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/url_params')
def url_params():
    params = request.args
    return render_template('url_params.html', params=params)

@app.route('/headers')
def headers():
    headers = dict(request.headers)
    return render_template('headers.html', headers=headers)

@app.route('/cookies')
def cookies():
    cookies = request.cookies
    response = make_response(render_template('cookies.html', cookies=cookies))
    
    # Check if our special cookie exists
    if 'special_cookie' in cookies:
        # If it exists, delete it
        response.delete_cookie('special_cookie')
    else:
        # If it doesn't exist, set it
        response.set_cookie('special_cookie', 'cookie_value')
    
    return response

@app.route('/form_params', methods=['GET', 'POST'])
def form_params():
    if request.method == 'POST':
        form_data = request.form
        return render_template('form_params.html', form_data=form_data)
    return render_template('form_params.html')

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted_number = None
    
    if request.method == 'POST':
        phone_number = request.form.get('phone', '')
        
        # Remove all allowed special characters
        digits_only = re.sub(r'[\s\(\)\-\.\+]', '', phone_number)
        
        # Check for invalid characters
        if not re.match(r'^[\d\s\(\)\-\.\+]+$', phone_number):
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
        else:
            # Check length based on prefix
            if phone_number.startswith(('+7', '8')):
                if len(digits_only) != 11:
                    error = 'Недопустимый ввод. Неверное количество цифр.'
                else:
                    # Format as 8-***-***-**-**
                    formatted_number = f"8-{digits_only[1:4]}-{digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
            else:
                if len(digits_only) != 10:
                    error = 'Недопустимый ввод. Неверное количество цифр.'
                else:
                    # Format as 8-***-***-**-**
                    formatted_number = f"8-{digits_only[0:3]}-{digits_only[3:6]}-{digits_only[6:8]}-{digits_only[8:10]}"
    
    return render_template('phone.html', error=error, formatted_number=formatted_number)

if __name__ == '__main__':
    app.run(debug=True) 