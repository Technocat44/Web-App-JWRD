const socket = new WebSocket("ws://" + location.host + "/ws");

console.log("this is establishing a websocket", socket)

// the socket event  
socket.onopen = function() {
  alert("[open] Connection established");
  // this will create a list of active and inactive users
  getAllUsers(); 
  for (const user in listOfActiveUsers){
    const idFromObj = user["id"];
    const htmlUserId = document.getElementById(idFromObj);
    console.log("this is teh id from the obj", idFromObj)
    console.log("this is the active user", user)
    // make the user active dot green
    
  } 
}
function sendToServer(user){
  socket.send("Sending some stuff");
  socket.send(JSON.stringify(user));
}

// want to write a function that gets all the users from the database
// 1. we need to get all users
// 2. check if the user is active, create a list of active users
// 3. if they are not active       create a list of inactive users
function getAllUsers() {
  const request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      const allusers = JSON.parse(this.response);
      console.log("all the users",allusers)
      for (const users in allusers){
        console.log("these are the users", users);
        sendToServer(users);
      }
    }
  };
  request.open("GET", "/allUsers");
  request.send();
 

}
  
// Now after getAllUsers() we have a list of all active and inactive users
// now we can grab each users document.getElementById and using websockets update their active button
/*
write a function in js that is on an interval and checks the active cookie
if there is a cookie that is expired, the event is triggered. Then we call
get all active users again and make two new list and then we can send the data over the websocket
*/
// If you want to find the value of one specified cookie, you must write a
// JavaScript function that searches for the cookie value in the cookie string.




