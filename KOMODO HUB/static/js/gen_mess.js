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

const BoxA = document.getElementById("BoxA");
const Mess_btn = document.getElementById("Mess_btn");
const Close_Mess = document.getElementById("Close_Mess");
const openBtn = document.getElementById("PersonA");
const openBtn2 = document.getElementById("PersonB");
const closeBtn = document.getElementById("close");
const closeBtn2 = document.getElementById("close2");
const modal = document.getElementById("modal");
const modal2 = document.getElementById("modal2")

Mess_btn.addEventListener("click", () =>{
    BoxA.classList.add("open");
});
Close_Mess.addEventListener("click", () =>{
    BoxA.classList.remove("open");
    modal.classList.remove("open");
    modal2.classList.remove("open");
})
openBtn.addEventListener("click", () => {
    modal.classList.add("open");
});
openBtn2.addEventListener("click", () => {
    modal2.classList.add("open");
});
closeBtn.addEventListener("click", () =>{
    modal.classList.remove("open");
});
closeBtn2.addEventListener("click", () =>{
    modal2.classList.remove("open");
});