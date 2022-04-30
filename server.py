# this makes the webapp folder a package and we can import it anywhere else in our code easily 
from flask import Flask
from webapp import create_app, views, auth, upload, images, messages, users


app = create_app()
    # Now that we have created and defined BLUEPRINTS we need to import these Blueprints 
#                  # the name of the Blueprint is views, auth
#from .views import viewer # this is importing the views file that is in the same directory and we import the blueprint
#from .auth import auther
# Now that we imported them we have to register them
app.register_blueprint(views.viewer, url_prefix='/')
app.register_blueprint(auth.auther, url_prefix='/')
app.register_blueprint(upload.uploader, url_prefix='/')
app.register_blueprint(messages.messager, url_prefix='/')
app.register_blueprint(users.usersGiver, url_prefix='/')

if __name__ == '__main__':
    # having debug set to True is important. The server will reload itself if the code change instead of having to do it
    # manually. 
    #      host,    port, debug
  # user_session = Session()
   app.run("0.0.0.0",5000, True)