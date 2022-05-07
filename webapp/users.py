from flask import Blueprint, render_template,request, flash, session, blueprints
from webapp.database import get_all_users


usersGiver = Blueprint("users", __name__)

@usersGiver.route('/users')
def usersHandler():
    defaultPicture = 'https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png'
    users = get_all_users()
    toSend = []
    for user in users:
        # print(user)
        if user.get('login') == True:
            userSend = {}
            userSend['id'] = user['id']
            userSend['username'] = user['username']
            if user.get('profilePic') != None:
                userSend['profilePic'] = user['profilePic']
            else:
                userSend['profilePic'] = defaultPicture
            userSend['description'] = user.get('description', '')
            toSend.append(userSend)
    # print(1)
    # print(toSend)
    return render_template("users.html", users = toSend)

@usersGiver.route('/allUsers')
def allUsers():
    users = get_all_users()
    toSend = []
    for user in users:
        if user.get('login') == True:
            toSend.append(user)
    return toSend

@usersGiver.route('/handleMessage', methods = ["POST"])
def handleMessageForm():
    return