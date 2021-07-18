from pluginFramework.pluginCollection import PluginCollection
from dotenv import load_dotenv
from multiprocessing import Process
import threading
import os
import twitch
import zmq

def messageHandler(message, socket):
  parsedMessage = message.text.split()
  if (parsedMessage[0][0] == '!'):
    socket.send_string(message.text)

def server(twitchChatInstance, port):
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind("tcp://*:%s" % port)
  twitchChatInstance.subscribe(lambda message: messageHandler(message, socket))

if __name__ == '__main__':
  plugins = PluginCollection('features')
  load_dotenv()
  oauthToken = os.environ.get("oauth-token")
  port = os.environ.get("port")
  int(port)
  twitchChatInstance = twitch.Chat(channel='#platypappas', nickname='platybotty', oauth=oauthToken)

  for plugin in plugins.plugins:
    feature = plugin(twitchChatInstance, port)
    threading.Thread(target=feature.runFeature, args=()).start()
  
  server(twitchChatInstance, port)
