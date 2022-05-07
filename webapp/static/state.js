var idToMessage = null

function get_chat_history(idToMessage) {
   const request = new XMLHttpRequest()
   request.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
         // const messages = JSON.parse(this.response)
         // for (const message of messages) {
         //    addMessage(message)
         // }
         const response = JSON.parse(this.response)
         console.log('received back: ', response)
      }
   }
   request.open('POST', '/fetchMessages')
   request.setRequestHeader("Content-Type", "application/json")
   request.send(toString(idToMessage))
}

function openMessages() {
   var x = document.getElementById('messageWindow')
   x.style.display = 'flex'
}

function handleOpen(e) {
   idToMessage = parseInt(e.parentElement.parentElement.id)
   get_chat_history(idToMessage)
   openMessages()
}

function closeMessages() {
   var x = document.getElementById('messageWindow')
   x.style.display = 'none'
}
