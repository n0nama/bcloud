var express = require('express');
var sockjs  = require('sockjs');
var http    = require('http');
var redis   = require('redis');

var sockjs_example = sockjs.createServer(
    {sockjs_url: "sockjs-0.3.min.js"}
);

sockjs_example.on('connection', function(connection) {
    var client = redis.createClient();

    connection.on('data', function(message) {
    	var a=JSON.parse(message);
    	if ('id' in a){
    		var channel_id=a.id;
	    	console.log(channel_id);
	    	client.subscribe(channel_id);
	    	client.on("message", function(channel, message){
        		connection.write(message);
        		console.log(message);
    		});
    		connection.on('close', function() {
		    	console.log('close')
		    	client.end();
		    });
	    }
    });
});

var my_app = express();
var server = http.createServer(my_app);

sockjs_example.installHandlers(server,
    {prefix:'/chat_socket'}
);

server.listen(5000, '192.168.0.59');