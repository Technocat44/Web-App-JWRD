from flask import Blueprint, render_template,request
from flask import Flask, render_template, request, redirect, url_for

from webapp.database import insertProfilePic
from .database import getPhotos, getImageFileID,insertImages, get_user_collection_via_auth_token
from .templeter import createList

accounter = Blueprint('account', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@accounter.route('/account', methods=['GET', 'POST'])
def home():
    token = request.cookies.get('auth_token',-1)
    username = get_user_collection_via_auth_token(token)
    if len(request.get_data()) != 0 and token != -1:
        print(len(request.files.get('upload').filename))
        if len(request.files.get('upload').filename):
        #print(request.form)
        #print(request.files)
            print(request.get_data())
            bite = (request.get_data().split(b'image/jpeg'))
            bite = bite[1].split(b'-------WebKit')
            bite = bite[0][4:-2]
            #print(bite)
            id = getImageFileID()
            insertProfilePic(id,username)
            with open('webapp/static/images/image-' + str(id) + '.jpg', 'wb') as file:
                file.write(bite)
                file.close()
            #imageList = getPhotos()
            imLen = int(len(imageList))
            #return render_template('upload.html', boolean=False, imList= imageList)
        else:
            imageList = getPhotos()
            return render_template('upload.html', boolean=False)
    imageList = getPhotos()
    return render_template('account.html', boolean=False)