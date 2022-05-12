var idToMessage = null

function removeAllChildNodes(parent) {
   while (parent.children.length > 1) {
      parent.removeChild(document.getElementById('messageInstanceClone'))
   }
}

function sendMessage() {
   const message = document.getElementById('inputSend').value
   document.getElementById('inputSend').value = ''
   const request = new XMLHttpRequest()
   request.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
         // const messages = JSON.parse(this.response)
         // for (const message of messages) {
         //    addMessage(message)
         // }
         const response = JSON.parse(this.response)
         console.log('received back: ', response)
         if (response.id == -1) {
            alert('Please Log In or Sign Up first!')
         } else {
            console.log(response.messages)
            openMessages(response.messages)
         }
      }
   }
   request.open('POST', '/handleMessage')
   request.setRequestHeader('Content-Type', 'application/json')
   request.send(JSON.stringify({ message: message }))
}

function get_chat_history() {
   const request = new XMLHttpRequest()
   request.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
         // const messages = JSON.parse(this.response)
         // for (const message of messages) {
         //    addMessage(message)
         // }
         const response = JSON.parse(this.response)
         console.log('received back: ', response)
         if (response.id == -1) {
            alert('Please Log In or Sign Up first!')
         } else {
            openMessages(response.messages)
         }
      }
   }
   request.open('POST', '/fetchMessages')
   request.setRequestHeader('Content-Type', 'application/json')
   console.log(idToMessage)
   if (idToMessage == null) {
      request.send(JSON.stringify({ id: -1 }))
   } else {
      request.send(JSON.stringify({ id: parseInt(idToMessage) }))
   }
}

function openMessages(messages) {
   var x = document.getElementById('messageWindow')
   x.style.display = 'flex'
   removeAllChildNodes(document.getElementById('messageWindow_messages_list'))
   const messageInstance = document.getElementById('messageInstance')
   messageInstance.style.display = 'none'
   console.log('messages are: ', messages)
   for (message of messages) {
      const clone = messageInstance.cloneNode(true)
      clone.style.display = 'block'
      clone.id = 'messageInstanceClone'
      clone.appendChild(document.createTextNode(message['user']+': '+message['message']))
      document.getElementById('messageWindow_messages_list').appendChild(clone)
   }
}

function handleOpen(e) {
   idToMessage = parseInt(e.parentElement.parentElement.id)
   console.log(idToMessage)
   get_chat_history(idToMessage)
}

function closeMessages() {
   var x = document.getElementById('messageWindow')
   x.style.display = 'none'
}
