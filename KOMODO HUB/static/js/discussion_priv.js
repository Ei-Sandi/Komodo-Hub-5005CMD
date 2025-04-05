var socket = io.connect("http://localhost:5000");

      
function sendMessage() {
    let message = document.getElementById("message").value;
    if (message.trim() === "") return;
    
    socket.emit('message', {message: message});
    document.getElementById("message").value = "";
}

socket.on('new_message', function(data) {
  let chatBox = document.getElementById("chat-box");

  let newMessageHTML = `
      <div class="message-box" id="msg-${data.cmt_id}">
          <p>${data.username}: ${data.message}</p>
          <small>(${data.timestamp})</small>
          ${data.username === "{{ current_user.username }}" ? 
              `<button class="delete-btn" onclick="deleteComment(${data.cmt_id})">X</button>` : ""
          }
      </div>
  `;

  chatBox.insertAdjacentHTML('afterbegin', newMessageHTML);
});

function deleteComment(commentId) {
    socket.emit('delete_message', { cmt_id: commentId });  
}

socket.on('message_deleted', function(data) {
    const msgElement = document.getElementById(`msg-${data.cmt_id}`);
    if (msgElement) {
        msgElement.remove();
    }
});

function showReplyBox(id) {
    document.getElementById("reply-box-" + id).style.display = "block";
}

function sendReply(replyId) {
    let input = document.getElementById("reply-input-" + replyId);
    let message = input.value;
    if (message.trim() === "") return;
    
    socket.emit('message', { message: message, reply_id: replyId });
    input.value = "";
    document.getElementById("reply-box-" + replyId).style.display = "none";
}


