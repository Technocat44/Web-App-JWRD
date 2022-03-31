# this makes the webapp folder a package and we can import it anywhere else in our code easily 
from flask import Flask


def create_app():
    app = Flask(__name__)
    # __name__ is the name of the current Python module. 
    # The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
    app.config['SECRET_KEY'] = 'dev'

    # SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during 
    # development, but it should be overridden with a random value when deploying.
    # Now that we have created and defined BLUEPRINTS we need to import these Blueprints 
    #                  # the name of the Blueprint is views, auth
    from .views import views # this is importing the views file that is in the same directory and we import the blueprint
    from .auth import auth
    # Now that we imported them we have to register them
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix ='/')

    
    return app

