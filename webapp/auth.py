from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from webapp.database import check_if_user_exist_on_signup, create_user_in_db, list_all, find_one
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

auther = Blueprint('auth', __name__)

# to allow different types of request for each route, we can add the methods parameter that takes a list with the type of request
#@auther.before_request()
@auther.route('/login', methods=['GET', 'POST'])
def login():
    """
    A session is used to store information related to a user, across different requests, as they interact with a web app.
    
    """
    if 'username' in session:
        render_template('home.html', boolean=True, user=session['username'])
    """
    A sessiom object works pretty much like an ordinary dict, with the difference that it keeps track of modifications.]
    A session allows you to store information specific to a user from one request to the next.
    In Flask, you can store information specific to a user for the duration of a session. Saving data for use throughout 
    a session allows the web app to keep data persistent over multiple requests 
    -- i.e., as a user accesses different pages within a web app.
    """
    
    """
    importing request allows us to access the data that was sent to this route.
    if we print(data) when we submit the form we will get an ImmutableDict object that stores the data!
        Example:
            ImmutableMultiDict([('email', 'jamesaqu@buffalo.edu'), ('password', '1234')])
    """
    if request.method == 'POST':
        # grab the data the client sent. 
        data = request.form
        print(data)
        email = request.form.get('email')
        password = request.form.get('password')

        if len(email) < 4:
            flash("Email must be longer than 4 characters.", category='error')
        elif len(password) < 7:
            flash("Passwords must be 8 characters or more.", category='error')
        else:
            flash("Successfully Logged in!")
            session["username"] = find_one(email)["fName"]
            return render_template('home.html', boolean=True, user=session["username"])
            

    return render_template('login.html', boolean=False, user=request.form.get('username'))

# adding a user parameter to the render_template allows us to pass in a value to be dealt with by the html template
@auther.route('/logout')
def logout():
    # I added this function call to make sure that its working properly, you can see the output in the terminal
    list_all()
    flash("Successfully Logged out!")
    return render_template('logout.html', user="Ryan")

@auther.route('/sign-up', methods=['GET','POST'])
def sign_up():
    username = None
    # grab the users_collection from the db
    if request.method == 'POST':
        data = request.form
        print(data)

        """
        Example of form data:
            ImmutableMultiDict([
                ('email', 'jamesaqu@buffalo.edu'),
                ('username', 'James'), 
                ('password1', '1234'), 
                ('password2', '1234')])
        """
        email = request.form.get('email')
        username = request.form.get('username')
        passwordOne = request.form.get('password1')
        passwordTwo = request.form.get('password2')
        
        # Super cool feature of Flask that allows us to respond to a user on malformed input 
        # https://www.tutorialspoint.com/flask/flask_message_flashing.htm
        if len(email) < 4:
            flash("Email must be longer than 4 characters.", category='error')
        elif len(username) < 2:
            flash("Name must be longer than 2 characters.", category='error')
        elif passwordOne != passwordTwo:
            flash("Passwords do not match, try again.", category='error')
        elif len(passwordOne) < 7:
            flash("Passwords must be 8 characters or more.", category='error')
        else:
            # add user to database
            # set up a new collection that stores the auth_token, username, email, password and salt
            """
            username = Exact same username the user created on sign up
                add a check to see if the username already exist, if it does flash the user to make a new one
            password = password if it is 8 characters long and the two passwords entered match
                generate some salt, append it to the password, hash it and store it in the database
            email = standard email

            auth_token = empty until user logs in

            salt = random string to append to the plaintext username


            user_collection example =
            {"username": "jamesaqu", "email": "jamesaqu@buffalo.edu",  "password": "$2js7fng84n7ab7fb949", "id": number
               will be blank on sign up[[ "auth_token": "$hah7jie9se48ei" ]] }
            """
            existing_user = check_if_user_exist_on_signup(username)
            if existing_user: # if the user exist we want to flash a message and tell the person signing up to try again
                flash("Username already exists, Please try again", category="error")
            else: # there is no username match in the database, so create a new user
                """
                When the user gives you their password (in the sign-up phase), hash it and then save the hash to the database. 
                When the user logs in, create the hash from the entered password and then compare it with the hash 
                stored in the database. If they match, log in the user. Otherwise, display an error message.
                function : check_password_hash(password_hash, password)

                """
                hash = bcrypt.generate_password_hash(passwordOne, 15)
                print("this is the hashed salted password: ", hash)
                create_user_in_db(username, email, hash)
                
                
    
                session["username"] = username
                flash("Account created", category='success')
                return redirect(url_for('views.home'))

            

   
    return render_template('sign-up.html')
  
"""
To authenticate users, Flask-Login requires you implement a handful special methods in the User class. 
The following table lists the required methods:
Method	            Description
is_authenticated()	returns True if user is authenticated (i.e logged in). Otherwise False.
is_active()	        returns True if account is not suspended. Otherwise False.
is_anonymous()	    returns True for anonymous users (i.e users who are not logged in). Otherwise False.
get_id()	        returns a unique identifier for the User object.
"""