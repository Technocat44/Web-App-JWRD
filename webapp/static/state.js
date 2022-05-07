function get_chat_history() {
   const request = new XMLHttpRequest()
   request.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
         // const messages = JSON.parse(this.response)
         // for (const message of messages) {
         //    addMessage(message)
         // }
         console.log('received back!')
      }
   }
   request.open('GET', '/fetchMessages')
   request.send()
}

function openMessages() {
   var x = document.getElementById('messageWindow')
   x.style.display = 'flex'
}

function handleOpen() {
   get_chat_history()
   openMessages()
}

function closeMessages() {
   var x = document.getElementById('messageWindow')
   x.style.display = 'none'
}
