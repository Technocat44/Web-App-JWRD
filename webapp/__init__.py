from flask import Flask
from flask_pymongo import PyMongo


# __name__ is the name of the current Python module. 
# The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
app = Flask(__name__) 
# SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during 
# development, but it should be overridden with a random value when deploying.
app.config['SECRET_KEY'] = 'dev'
app.config["MONGO_URI"] = "mongodb+srv://devUser:jesseHartloff@clusterjwrd.49opx.mongodb.net/JWRD_DB?retryWrites=true&w=majority"
mongo_client = PyMongo()
mongo_client.init_app(app)


