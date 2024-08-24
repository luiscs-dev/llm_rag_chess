var socket = io();

socket.on('message', function(msg) {
    $('#messages').append($('<li>').text(msg));
});

function sendMessage() {
    socket.send($('#message').val());
    $('#message').val('');
}
