from flask import Blueprint, render_template,request
from flask import Flask, render_template, request, redirect, url_for
from .database import getPhotos, getImageFileID,insertImages
from .templeter import createList

uploader = Blueprint('upload', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@uploader.route('/upload', methods=['GET', 'POST'])
def home():
    if len(request.get_data()) != 0:
        print(len(request.files.get('upload').filename))
        if len(request.files.get('upload').filename):
        #print(request.form)
        #print(request.files)
            bite = (request.get_data().split(b'image/jpeg'))
            bite = bite[1].split(b'----')
            bite = bite[0][4:-2]
            #print(bite)
            id = getImageFileID()
            insertImages(id)
            with open('webapp/static/images/image-' + str(id) + '.jpg', 'wb') as file:
                file.write(bite)
                file.close()
            imageList = getPhotos()
            imLen = int(len(imageList))
            return render_template('upload.html', boolean=False, imList= imageList)
        else:
            imageList = getPhotos()
            return render_template('upload.html', boolean=False, imList= imageList)
    imageList = getPhotos()
    return render_template('upload.html', boolean=False, imList= imageList)