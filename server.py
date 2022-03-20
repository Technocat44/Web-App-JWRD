from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

if __name__ == '__main__':
        #   host,    port, debug
   app.run("0.0.0.0",5000, False)