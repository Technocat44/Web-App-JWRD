from flask import Blueprint, request
import time

websocker = Blueprint('websockets', __name__)


# the websocket path
@websocker.route("/ws")
def sock(ws):
  while True:
      data = ws.receive()
      ws.send(data)
      time.sleep(.10)