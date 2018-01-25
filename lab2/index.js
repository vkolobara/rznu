var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var people = {};

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
    socket.on('message', function (msg) {
        console.log(people[socket.id] + " " + msg);
        io.emit("message", people[socket.id], msg);
    });
    socket.on('login', function (name) {
        console.log("LOGIN: " + name)
        people[socket.id] = name;
        io.emit('adminMessage', people[socket.id] + " joined the conversation!");
    });
    socket.on('disconnect', function () {
        console.log("disconnect: " + people[socket.id]);
        io.emit('adminMessage', people[socket.id] + " left the conversation!");
        delete people[socket.id];
    });
});

http.listen(666, function () {
    console.log('listening on localhost:666');
});

