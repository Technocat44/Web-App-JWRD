from flask import Blueprint, render_template,request, flash
from webapp.database import add_message,list_messages


messager = Blueprint("message", __name__)

@messager.route("/message", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        # this is sending a message
        #d.add_message(,request.form.get("receiver"), request.form.get("message"))
        add_message("user1", "user2", "hellooo")
        add_message("user2", "user1", "hiya")
        add_message("user3", "user1", "hello")
        add_message("user1", "user3", "yurr")
    return render_template("messages.html", length = 0, messages = [])

    

def escapeHTML(message):
    m = message.replace("&", "&amp")
    m = m.replace("<", "&lt")
    return m.replace(">", "&gt")