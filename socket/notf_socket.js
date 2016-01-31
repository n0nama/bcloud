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
        if ('id' in a) {
            console.log(a.id);
            var channel_id = a.id;
            client.subscribe(channel_id);
            client.on("message", function (channel, message) {
                connection.write(message);
            });
        };
    });
    connection.on('close', function () {
        console.log('disconnect');
        client.end();
    });
});

var my_app = express();
my_app.use(cors());

var server = http.createServer(my_app);

sockjs_example.installHandlers(server,
    {prefix:'/notf_socket'}
);

server.listen(5000, '108.61.199.8');