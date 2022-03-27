from webapp import create_app

app = create_app()

# @app.route('/')
# def greetings():
#    return "Greetings!"

# @app.route("/hello")
# def hello_world():
#    return "hello world"

if __name__ == '__main__':
    # having debug set to True is important. The server will reload itself if the code change instead of having to do it
    # manually. 
    #      host,    port, debug
   app.run("0.0.0.0",5000, True)