// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const chatBox = document.getElementById("message");
    const comment = chatBox.value;
    const receiver = document.getElementById("receiver");
    const received = receiver.value;
    chatBox.value = "";
    receiver.value= "";
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({'receiver':received, 'messageType': 'chatMessage', 'comment': comment}));
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}

// called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessage(message);
            }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType

    switch (messageType) {
        case 'chatMessage':
            addMessage(message);
            break;
        default:
            console.log("received an invalid WS messageType");
    }
}