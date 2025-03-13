$(document).ready(function(){
    // var socket = io.connect("http://192.168.1.108:5000")
    var socket = io.connect("http://localhost:5000")
    // socket.on('connect', function() {
    //     socket.send("Connected")
    // });

    socket.on('message', function(msg){
        $('#MessageBox').append('<li>'+msg+'</li>');
    });

    $('#S_btn').on('click', function(){
        socket.send($('#UserName').val() + ': ' + $('#Message').val());
        $('#Message').val('');
    });
});

const BoxA = document.getElementById("BoxA");
const Mess_btn = document.getElementById("Mess_btn");
const Close_Mess = document.getElementById("Close_Mess");
const openBtn = document.getElementById("PersonA");
const closeBtn = document.getElementById("close");
const modal = document.getElementById("modal");

Mess_btn.addEventListener("click", () =>{
    BoxA.classList.add("open");
});
Close_Mess.addEventListener("click", () =>{
    BoxA.classList.remove("open");
})
openBtn.addEventListener("click", () => {
    modal.classList.add("open");
});
closeBtn.addEventListener("click", () =>{
    modal.classList.remove("open");
})