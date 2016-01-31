var express = require('express');
var sockjs  = require('sockjs');
var http    = require('http');
var redis   = require('redis');
var cors    = require('cors');

var sockjs_example = sockjs.createServer(
    {sockjs_url: "sockjs-0.3.min.js"}
);

sockjs_example.on('connection', function(connection) {
    var client = redis.createClient();

    connection.on('data', function(message) {
    	var a=JSON.parse(message);
        if ('id' in a && 'auth_key' in a){
            client.get(a.id, function(err, value){
                console.log(value);
                console.log(a.auth_key);
                if (value == a.auth_key){
                    console.log('Q');
                    var channel_id=a.id;
                    client.subscribe(channel_id);
                    client.on("message", function(channel, message){
                        connection.write(message);
                    });
                    connection.on('close', function() {
                        client.end();
                    });
                }
                else{
                    console.log('Hacked');
                    client.end();
                    connection.close();
                }
            });

        };
    });
});

var my_app = express();
my_app.use(cors());

var server = http.createServer(my_app);

sockjs_example.installHandlers(server,
    {prefix:'/chat_socket'}
);

server.listen(5000, '108.61.199.8');
