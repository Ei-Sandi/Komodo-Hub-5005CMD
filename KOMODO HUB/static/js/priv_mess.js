const {room} = Qs.parse(location.search, {
    ignoreQueryPrefix: true
});

console.log(room)

$(document).ready(function(){
    // var socket = io.connect("http://192.168.1.108:5000");
    var socket = io.connect("http://localhost:5000");

    socket.on('message', function(msg){
        $('#message_history').append('<li>'+msg+'</li>');
        console.log('Recieved');
    });

    $('#send').on('click', function(){
        socket.send(': ' + $('#chat_message').val());
        $('#chat_message').val('');
        console.log('Sent');
    });
});
