from flask import Blueprint, render_template,request, flash, session, blueprints, send_file
from webapp.database import add_message, list_messages, add_user_sid, delete_user_sid, find_user_sid
from webapp.__init__ import socketio
from flask_socketio import emit, send
from webapp.models import user_session
import json
from flask_socketio import send, join_room, leave_room, emit

messager = Blueprint("message", __name__)
receiver = ''
username = ''

@messager.route('/message', methods = ['GET', 'POST'])
def home():
    receiver = ''
    if request.method == 'POST':
        # this is sending a message
        #d.add_message(,request.form.get("receiver"), request.form.get("message"))
        receiver = request.form.get('receiver')
        msg = request.form.get('message')
        username = "username1"
        if username != None:
            add_message(username, receiver, escapeHTML(msg))
            messages = list_messages(username, receiver)
            return render_template("messages.html", msgs = messages)
    return render_template('messages.html', msgs=[])




def escapeHTML(message):
    m = message.replace("&", "&amp")
    m = m.replace("<", "&lt")
    return m.replace(">", "&gt")