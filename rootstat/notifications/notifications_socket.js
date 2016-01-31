var recInterval = null;
var socket = null;

/*var open_socket = function() {
    socket = new SockJS('http://108.61.199.8:5000/notf_socket');
    clearInterval(recInterval);
    socket.onopen = function() {
        send_user_id(user_id)
    };
    socket.onclose = function() {
          socket = null;
          recInterval = setInterval(function() {
              open_socket();
          }, 5000);
    };
};*/

function send_user_id(user_id){
    socket.send(JSON.stringify({'id': user_id}));
    socket.onmessage = function(e){
        messages_handler(e.data);
    };
};