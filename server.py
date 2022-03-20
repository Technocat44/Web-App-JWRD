from flask import Flask # have to import the Flask Class from the flash moduel
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

if __name__ == '__main__':
    #      host,    port, debug
    # having debug set to True is important. The server will reload itself if the code change instead of having to do it
    # manually. 
   app.run("0.0.0.0",5000, True)