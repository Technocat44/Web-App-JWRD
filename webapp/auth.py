# from nis import cat
from flask import Blueprint, make_response, redirect, render_template, request, flash, url_for
from webapp.database import add_auth_token_to_users_collection, check_if_user_exist_on_signup, create_user_in_db, list_all, retrieve_hashed_auth_token_from_db, retrieve_user\
    ,add_auth_token_to_users_collection, set_user_login_to_true, get_user_collection_via_auth_token, update_auth_token_to_None ,update_login_to_False\
        ,update_auth_token_to_None
import secrets
import bcrypt
import hashlib
# from webapp.models import user_session

# bcrypt = Bcrypt()

auther = Blueprint('auth', __name__)


# to allow different types of request for each route, we can add the methods parameter that takes a list with the type of request
#@auther.before_request()
@auther.route('/login', methods=['GET', 'POST'])
def login():
   
    # global user_session
    # if user_session.get_login():
    #     flash("Already logged in")
    #     return redirect(url_for('views.home'))

    """
    A session is used to store information related to a user, across different requests, as they interact with a web app.
    
    # """
    # if 'username' in session:
    #     render_template('home.html', boolean=True, user=session['username'])
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
        print("we are in the post of /login")
        # grab the data the client sent. 
        data = request.form
        print(data)
        username = request.form.get('username')
        print("this is the username from login page: ", username)
        password = request.form.get('password')
        print("this is the password from the login page ", password)

        print("this is the password: ", password)
        if len(password) < 7:
            flash("Passwords must be 8 characters or more.", category='error')
            return redirect(url_for('auth.login'))

        else:
            userFromDB = retrieve_user(username)
            print("this is the user from the db, should be False or the user dict: ", userFromDB)

            if not userFromDB:
                print("yes there is no userName")
                flash("Incorrect username", category='error')
                return redirect(url_for('auth.login'))

            # check if password matches
            else:
                print("entering else")
                saltFromDB = userFromDB["salt"]         # grab salt from userFromDB
                print("this is the salt  : ",saltFromDB)

                passwordhashFromDB = userFromDB["password"] # grab hashed password from db
                print("this is the password from database : ",passwordhashFromDB)

                loginhash = bcrypt.hashpw(password.encode(), saltFromDB) # create a hash from the salt and the login password attempt
                print("this is the new hash from the login password : ",loginhash)

                if loginhash != passwordhashFromDB:
                    flash("Incorrect password, try again", category='error')
                    return redirect(url_for('auth.login'))
                new_auth_token = secrets.token_urlsafe(50)  # need to generate auth tokens
                print("this is the auth token : ",new_auth_token)

                hash_of_auth_token_cookie = hashlib.sha256(new_auth_token.encode()).hexdigest()
                print("/login this is the hash_of the new auth token", hash_of_auth_token_cookie)
               # hash_token = hashlib.sha256(new_auth_token.encode()).hexdigest() # hash the auth_token and store it in db
                add_auth_token_to_users_collection(hash_of_auth_token_cookie, userFromDB) # need to update users_collection with the auth token for the user logging in.

                # grabbing_hash = get_user_collection_via_auth_token(new_auth_token)
                # print("/login, right after storing the hased auth_token, I am retrieving the same auth token from db", grabbing_hash["username"])
                # # update user_collection to set login to True
                set_user_login_to_true(userFromDB["username"],True)
                

                
                print("before the user sets anything")
                
                # user_session.print_session_state()
                # user_session.set_username(username)
                # user_session.set_login(True)
                # I want to set the auth-token to the one set in the database
                print("after we set some of the session data")
                # user_session.print_session_state()
                
                # session["username"] = username 
                # TODO: want to add user_session to a collection in the database to keep track of who is logged in

                # from webapp.database import add_user_session_to_db
                # add_user_session_to_db(user_session.get_username(), user_session.get_login())
                resp = make_response(render_template("home.html", boolean=True, user=userFromDB["username"])) # make a response variable
                resp.set_cookie("auth_token", new_auth_token, max_age=7200, httponly=True) # set the unhashed auth token in the cookie
        

              
                flash("Successfully Logged in!")
                return resp
    print("user already has been been logged in /login")
    auth_token_cookie = request.cookies.get("auth_token", -1)
    # hash it so I can search for it in the database
    print("this is the auth_token_cookie in /login", auth_token_cookie)
    if auth_token_cookie == -1:
        return render_template("login.html", user=None)
    userVerifiedFromDatabase = get_user_collection_via_auth_token(auth_token_cookie)
    if userVerifiedFromDatabase == None:
        return render_template("login.html", user=None)
    set_user_login_to_true(userVerifiedFromDatabase["username"], True)
    print("this is the user from the db with a matching authtoken in /login")
    print(userVerifiedFromDatabase, flush =True)
    if userVerifiedFromDatabase == None:
        return render_template("login.html", user=None)
    return render_template('home.html', user=userVerifiedFromDatabase["username"])

# adding a user parameter to the render_template allows us to pass in a value to be dealt with by the html template
@auther.route('/logout')
def logout():
    # I added this function call to make sure that its working properly, you can see the output in the terminal
    # if user_session.get_login() == False:
    #     return   render_template('logout.html')

    # get current auth token from browser
    auth_token_cookie = request.cookies.get("auth_token", -1)
    # hash it so I can search for it in the database
    
    if auth_token_cookie == False:
        return render_template("home.html", user=None)
    userVerifiedFromDatabase = get_user_collection_via_auth_token(auth_token_cookie)
    print(userVerifiedFromDatabase, flush =True)
    if userVerifiedFromDatabase == None:
        return render_template("home.html", user=None)
    list_all()
    # goodbyeUser = user_session.get_username()
    # user_session.set_log_out()
    # user_session.print_session_state()
    #TODO: delete the auth token when logging out
    usernameToDisplayOnLogout = userVerifiedFromDatabase["username"]

    update_login_to_False(userVerifiedFromDatabase)
    update_auth_token_to_None(userVerifiedFromDatabase)
    flash("Successfully Logged out!")
    # TODO: I want to go into the logged_in collection in the database and remove the user who is logging out
    return render_template('logout.html', user=usernameToDisplayOnLogout)

        # when a user logs out, we need to set logout to true 
        # but we also want to wipe their session object
        # so before we wipe it, we grab the user name and store it in a variable, this way we can proceed to wipe the state
    # but still say good bye by passing the username variable we just created to user=<user variable> in render_template
    return render_template('logout.html', user=usernameToDisplayOnLogout)

@auther.route('/sign-up', methods=['GET','POST'])
def sign_up():

    #from webapp.database import retrieve_hashed_auth_token_from_db
    # want to change it to check the auth_token 
    
    # global user_session
    username = None
    auth_token_cookie = request.cookies.get("auth_token", -1)
    # if they already have an auth token, they dont need to sign up.
    # if they dont have an auth token (-1) then they have to sign up
    print("this is the auth_token_cookie: if not logged in, should be -1: ", auth_token_cookie)
    if auth_token_cookie == -1:
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
                    salt = bcrypt.gensalt(15)
                    hash = bcrypt.hashpw(passwordOne.encode(), salt)
                    login = False
                    profpic = None
                    print("this is the hashed salted password: ", hash)
                    create_user_in_db(email, username, hash, salt, login, profpic)
                    
                    
                    # session["username"] = username
                    flash("Account created", category='success')
                    return redirect(url_for('views.home'))

    else: 
        print("the user has an auth token")
        
        auth_token_from_Db = get_user_collection_via_auth_token(auth_token_cookie)
        if auth_token_from_Db:
            # print("this is the user_session variable: ", user_session)
            # print(user_session.print_session_state())
            try:
                flash("You might be logged in already", category='error')
                # print(user_session.get_username(), "this is what get_username returns after I logout")
                return render_template("sign-up.html", user=username)        

            except:
                return render_template("sign-up.html")        

        flash("Already logged in", category='error')
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