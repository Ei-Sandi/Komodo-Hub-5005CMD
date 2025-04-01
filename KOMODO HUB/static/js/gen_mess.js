$(document).ready(function(){
    // var socket = io.connect("http://192.168.1.108:5000");
    var socket = io.connect("http://localhost:5000");

    socket.on('message', function(msg){
        $('#MessageBox').append('<li>'+msg+'</li>');
        console.log('Recieved');
    });

    $('#S_btn').on('click', function(){
        socket.send(': ' + $('#Message').val());
        $('#Message').val('');
        console.log('Sent');
    });
});

//Check if account can join room
