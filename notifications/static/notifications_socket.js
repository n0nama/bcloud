connect_socket = function() {
    sokcet = new SockJS('http://108.61.199.8:5000/chat_socket');
};

function open_socket(){
    connect_socket()
    sokcet.onclose = setInterval(function(){
        console.log('Socket disconnected');
        connect_socket();
    }, 1500)
};

function connect_to(id){
    socket.send(JSON.stringify({'user_id': id}))
}

socket.onmessage(function(e){
    message_handler(e.data)
});