const socket = new WebSocket("ws://" + location.host + "/ws");

console.log("this is establishing a websocket", socket)

// the socket event  
socket.onopen = function() {
  alert("[open] Connection established");
  alert(document.cookie)
  // this will create a list of active and inactive users
  getSingleUser();
  getAllUsers(); 

    // make the user active dot green
}

function getSingleUser() {
  const request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      const username = JSON.parse(this.response);
      console.log("this is the single user",username)
    }
  };
  // grab the auth_cookie from the current user
  // open a post request to the single user path in users 
  // send tp the single user path with the auth token from the current user
  const auth_cookie = getCookie();
  console.log("AUTH COOKIE >>>" , auth_cookie)
  if (auth_cookie != "") {
    request.open('POST', '/singleUser');
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(auth_cookie));
  }
  
}

function sendToServer(user){
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
      for (const users of allusers){
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


socket.onclose = function() {

}

/*

Create a variable (name) with the text to search for (cookiename + "=").

Decode the cookie string, to handle cookies with special characters, e.g. '$'

Split document.cookie on semicolons into an array called cookieArray (cookieArray = decodedCookie.split(';')).

Loop through the cookieArray (i = 0; i < cookieArray.length; i++), and read out each value cookie = cookieArray[i]).

If the cookie is found (cookie.indexOf(name) == 0), return the value of the cookie (cookie.substring(name.length, cookie.length).

If the cookie is not found, return "".
*/
function getCookie() {
  let name = "auth_token" + "=";
  console.log(document.cookie)
  let decodedCookie = decodeURIComponent(document.cookie);
  console.log("decoded cookie >>>", decodedCookie)
  let cookieArray = decodedCookie.split(';');
  console.log("cookie array >>>", cookieArray)
  for(let i = 0; i <cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) == ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) == 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}