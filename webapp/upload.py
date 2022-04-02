from flask import Blueprint, render_template,request

uploader = Blueprint('upload', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@uploader.route('/upload', methods=['GET', 'POST'])
def home():
    return render_template('upload.html', boolean=False, user=request.form.get('firstName'))