from flask import Blueprint, request
import time

websocker = Blueprint('websockets', __name__)


# the websocket path
@websocker.route("/ws")
def sock(ws):
  while True:
      print("This is the ws data from inside websocket.py", ws)
      data = ws.receive()
      ws.send(data)
      