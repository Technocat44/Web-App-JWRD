from flask import Flask, Blueprint, render_template, request, redirect, url_for
from webapp.database import insertProfilePic, insertDesc
from webapp.database import getPhotos, getImageFileID,insertImages, get_user_collection_via_auth_token
from webapp.templeter import createList

accounter = Blueprint('account', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@accounter.route('/account', methods=['GET', 'POST'])
def home():
    token = request.cookies.get('auth_token',-1)
    if token != -1:
        username = get_user_collection_via_auth_token(token)
        if username != None:
            print(request.get_data(),flush=True)
            if request.get_data().__contains__(b'filename'):
                imageUpload(token,username)
            if request.get_data().__contains__(b'description'):
                descUpload(token,username)
    else: 
        print('didnt hit',flush=True)
    return render_template('account.html', boolean=False)



def imageUpload(token,username):
    if (request.get_data()) != 0 and token != -1:
        print(len(request.files.get('upload').filename))
        if len(request.files.get('upload').filename):
            #print(request.form)
            #print(request.files)
            #print(request.get_data())
            bite = (request.get_data().split(b'image/jpeg'))
            bite = bite[1].split(b'------')
            bite = bite[0][4:-2]
            #print(bite)
            id = getImageFileID()
            insertProfilePic(id,username)
            with open('webapp/static/images/image-' + str(id) + '.jpg', 'wb') as file:
                file.write(bite)
                file.close()
            #imageList = getPhotos()
            #imLen = int(len(imageList))
            return 0
        return -1

def descUpload(token,username):
    if (request.get_data()) != 0 and token != -1:
        #print(request.form)
        #print(request.files)
        #print(request.get_data())
        # splitter = (request.get_data().split(b'name=\"Content-Disposition\"'))[0][:-2]
        # print("SPLITTER:" + splitter.decode(),flush=True)
        bite = (request.get_data().split(b'name=\"description\"'))
        print('SPLIT 1:')
        print(bite)
        bite = bite[1].split(b'------')
        print('SPLIT 2:')
        print(bite,flush=True)
        bite = bite[0][4:-2]
        print('SPLIT 3:')
        print(bite,flush=True)
        insertDesc(bite.decode(),username)
        #imageList = getPhotos()
        #imLen = int(len(imageList))
        return 0
    return -1