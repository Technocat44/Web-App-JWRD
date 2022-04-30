from flask import Blueprint, render_template,request, flash, session, blueprints, send_file
from webapp.database import add_message,list_messages
from webapp.__init__ import socketio
from flask_socketio import emit, send
from webapp.models import user_session
import json

messager = Blueprint("message", __name__)

@messager.route('/message', methods = ['GET', 'POST'])
def home():
    receiver = ''
    if request.method == 'POST':
        # this is sending a message
        #d.add_message(,request.form.get("receiver"), request.form.get("message"))
        receiver = request.form.get('receiver')
        msg = request.form.get('message')
        username = user_session.get_username()
        if username != None:
            add_message(username, receiver, escapeHTML(msg))
            messages = list_messages(username, receiver)
            return render_template("messages.html", msgs = messages)
    return render_template('messages.html', msgs=[])

@socketio.on('join-chat')
def connect_private_chat(data):
    request.form.get("receiver")

def escapeHTML(message):
    m = message.replace("&", "&amp")
    m = m.replace("<", "&lt")
    return m.replace(">", "&gt")