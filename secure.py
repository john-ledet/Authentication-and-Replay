from flask import Flask, request, render_template, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'

#create some kind of mock database involving authentication; user : password
database = {"admin_john": "Goaggies012"}

#create a database that relates a user to a token for a successful login; user : token
tokens = {"admin_john" : "21"}

@app.route('/', methods = ['GET'])
def login_page():
    if 'user' in session:
        return redirect(url_for('token_authentication'))
    
    return render_template('login.html')

@app.route('/', methods = ['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    

    if user in database and database[user] == password :
        session['user'] = user
        token = tokens[user]
        return jsonify({"message": "Login success; go to /confidential route to access confidential data, use /logout to logout user out of the session", "token": token})
    else :
        return render_template('login.html', error = "invalid login info")
    
@app.route('/confidential', methods=['GET'])
def token_authentication():
    # Check if the user is logged in
    if 'user' not in session:
       return jsonify({"message": "You must log in to access this page"}), 401
    # Retrieve the logged-in user
    user = session['user']
    token = tokens.get(user)
    # Check if the token exists
    if token in tokens.values():
        return jsonify({"message": "Access granted to confidential data", "data": "Confidential data"})
    else:
        return jsonify({"message": "Access not granted to confidential data"}), 401

    
@app.route('/logout', methods=['GET'])
def logout():
    # Log the user out by clearing their session
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__' :
    app.run(debug=True)