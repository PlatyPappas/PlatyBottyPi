const tmi = require('tmi.js');
const zmq = require('zeromq');
require('dotenv').config();

//Set up pub socket - always publish incoming message
var pluginPubSocket = zmq.socket('pub');
pluginPubSocket.bind(`tcp://127.0.0.1:${process.env.pluginSubPort}`);

//Set up twitch instance
const client = new tmi.Client({
  connection: {
    secure: true,
    reconnect: true
  },
  identity: {
    username: 'PlatyBotty',
    password: `${process.env.oauth_token}`,
  },
  channels: ['platypappas']
});

client.connect();

client.on('message', (channel, tags, message, self) => {
  pluginPubSocket.send(message)
});

//Set up sub socket
var serverSubSocket = zmq.socket('rep');
serverSubSocket.connect(`tcp://127.0.0.1:${process.env.serverSubPort}`);

serverSubSocket.on('message', function (payload) {
  var data = JSON.parse(JSON.parse(payload));
  client.say('#platypappas', data["message"]);
  serverSubSocket.send("OK");
});