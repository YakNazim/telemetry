var net = require('net');
var wsock = require('websock');
var source_url = 'ws://localhost:8081/ws'
var octopus = require('websock').connect(source_url)

var clients = []

wsock.listen(8100, ws_connect);
console.log('listening 8100')

octopus.on('open', function() {
  console.log('octopus open!'+source_url);
})

octopus.on('message', function(data) {
  console.log('<-oc '+data)
  clients.forEach(function(client){
    client.send(data)
  })
});

octopus.on('error', function() {
  console.log('octopus error');
})

octopus.on('close', function() {
  console.log('octopus close');
})

function ws_connect(socket) {
  console.log('#*# ')
  console.log('#*# ws_connect')
  clients.push(socket)
  console.log('#*# client count '+clients.length)
  console.log('#*# ')

  socket.on('message', function(data) {
    console.log('<-ws '+data)
  });

  socket.on('close', function() {
    console.log('websockets close');
  });

}
