from flask import Blueprint, render_template,request, flash, session, blueprints
from webapp.database import add_message,list_messages


messager = Blueprint("message", __name__)

@messager.route('/message', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        # this is sending a message
        #d.add_message(,request.form.get("receiver"), request.form.get("message"))
        receiver = request.form.get('receiver')
        msg = request.form.get('message')
        add_message(session.get("username"), receiver, msg)
    #return render_template("templates/messages.html", length = len(list_messages("user1", "user2")), messages = list_messages("user1", "user2"))
    messages = list_messages("user1", "user2")
    return render_template("messages.html", msgs = messages)

def escapeHTML(message):
    m = message.replace("&", "&amp")
    m = m.replace("<", "&lt")
    return m.replace(">", "&gt")