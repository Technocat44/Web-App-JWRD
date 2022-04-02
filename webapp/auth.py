from flask import Blueprint, render_template, request, flash, session
from webapp.database import createUser, list_all, find_one
from flask_bcrypt import Bcrypt 


auther = Blueprint('auth', __name__)

# to allow different types of request for each route, we can add the methods parameter that takes a list with the type of request
@auther.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        render_template('login.html', boolean=True, user=session['username'])
    """
    A sessiom object works pretty much like an ordinary dict, with the difference that it keeps track of modifications.]
    A session allows you to store information specific to a user from one request to the next.
    """
    
    """
    importing request allows us to access the data that was sent to this route.
    if we print(data) when we submit the form we will get an ImmutableDict object that stores the data!
        Example:
            ImmutableMultiDict([('email', 'jamesaqu@buffalo.edu'), ('password', '1234')])
    """
    if request.method == 'POST':
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
            return render_template('home.html', boolean=True, user=request.form.get('firstName'))
            

    return render_template('login.html', boolean=False, user=request.form.get('firstName'))

# adding a user parameter to the render_template allows us to pass in a value to be dealt with by the html template
@auther.route('/logout')
def logout():
    # I added this function call to make sure that its working properly, you can see the output in the terminal
    list_all()
    flash("Successfully Logged out!")
    return render_template('logout.html', user="Ryan")

@auther.route('/sign-up', methods=['GET','POST'])
def sign_up():
    userName = None
    # grab the users_collection from the db
    

    if request.method == 'POST':
        data = request.form
        print(data)

        """
        Example of form data:
            ImmutableMultiDict([
                ('email', 'jamesaqu@buffalo.edu'),
                ('userName', 'James'), 
                ('password1', '1234'), 
                ('password2', '1234')])
        """
        email = request.form.get('email')
        userName = request.form.get('userName')
        passwordOne = request.form.get('password1')
        passwordTwo = request.form.get('password2')

        existing_user = find_one()
        if existing_user is None:
            hash = Bcrypt.generate_password_hash(passwordOne).decode('UTF-8')
            

        # Super cool feature of Flask that allows us to respond to a user on malformed input 
        # https://www.tutorialspoint.com/flask/flask_message_flashing.htm
        if len(email) < 4:
            flash("Email must be longer than 4 characters.", category='error')
        elif len(userName) < 2:
            flash("Name must be longer than 2 characters.", category='error')
        elif passwordOne != passwordTwo:
            flash("Passwords do not match, try again.", category='error')
        elif len(passwordOne) < 7:
            flash("Passwords must be 8 characters or more.", category='error')
        else:
            # add user to database
            createUser(email, userName, passwordOne) 

            flash("Account created", category='success')

    if userName != None:
        return render_template('sign-up.html', user=userName)
    else:
        return render_template('sign-up.html')
