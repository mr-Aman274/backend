// console.log('hello world')
// const socket = new WebSocket('ws://' + window.location.host + '/ws/search')
const WebSocket = require('ws');

const socket = new WebSocket('ws://127.0.0.1:8000/ws/search');
socket.addEventListener('open', function (event) {
    console.log('Connected to server');
  });

socket.onmessage = function(e) {
    console.log('Server : ' + e.data);
    
};

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'message': "hello from client1 ",
        'sender': 'websock1'
    }));
};

socket.addEventListener('close', function (event) {
  console.log('Connection closed');
});





// socket.addEventListener('message', function (event) {
//   console.log('Received message:', event.data);
// });

