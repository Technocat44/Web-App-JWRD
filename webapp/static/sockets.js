let socket = io.connect("http://localhost:5000");
let socket_messages = io.connect("http://localhost:5000/msgs");

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
    const userBox = document.getElementById("receiver");
    const username = userBox.value;
    chatBox.value = "";
    userBox.value = "";
    userBox.focus()
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({'receiver': username, 'comment': comment}));
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}

$(document).ready(function() {
    

    $('#send').on('click', function() {
        let message = $('#message').val();

        socket_messages.emit('msg_from_usr', message)
    });

    $('#send').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            let message = $('#message').val();
            socket_messages.emit('msg_from_usr', message)
        }
    });


})
