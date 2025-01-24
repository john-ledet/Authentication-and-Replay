from flask import Flask, request, render_template, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'

# Mock database for authentication; user : password
database = {"admin_john": "Goaggies012"}

# Constant token for all users (static and predictable)
constant_token = "21"

@app.route('/', methods=['GET'])
def login_page():
    if 'user' in session:
        # Automatically redirect logged-in users to confidential
        return redirect(url_for('token_authentication'))
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    
    # Check credentials
    if user in database and database[user] == password:
        session['user'] = user  # Log the user in
        # Return the constant token
        return jsonify({"message": "Login success; go to /confidential route to access confidential data", "token": constant_token})
    else:
        return render_template('login.html', error="Invalid login info")

@app.route('/confidential', methods=['GET'])
def token_authentication():
    # Check if the Authorization header contains the constant token
    token = request.headers.get("Authorization")
    if token == constant_token:
        # Access granted solely based on the constant token
        return jsonify({"message": "Access granted to confidential data", "data": "Confidential data"})
    else:
        return jsonify({"message": "Access not granted to confidential data"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    # Log the user out by clearing their session
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
