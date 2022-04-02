from flask import Blueprint, render_template,request


images = Blueprint('views', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@images.route('/image-1.jpg', methods=['GET','POST'])
def imager():
    if request.method == 'GET':
        print(request.method)
    return render_template("upload.html")