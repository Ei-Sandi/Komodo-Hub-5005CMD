var socket = io.connect("http://localhost:5000");

const chat_form = document.getElementById('chat_form');
const { userJoin, getCurrentUser } = require('./js/user');

// Username and room
const {username1 , username2} = Qs.parse(location.search, {
    ignoreQueryPrefix: true
});

console.log(username1, username2);

//Join room
socket.emit('joinRoom', { username1, username2});

socket.on('connect', function() {
    socket.emit('User connected');
});

socket.on('message', message =>{
    console.log('Message Sent');
});

chat_form.addEventListener('submit', (mess)=>{
    mess.preventDefault();
    
    const msg = mess.target.elements.chat_message.value;
    console.log(msg);
});