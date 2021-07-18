import zmq
import threading

class Plugin(object):

  def __init__(self, twitchChatInstance, port, description = 'UNKNOWN', command = 'UNKNOWN'):
    self.description = description
    self.command = command
    self.twitchChatInstance = twitchChatInstance
    self.subscribeToParent(port)

  def subscribeToParent(self, port):
    context = zmq.Context()
    self.socket = context.socket(zmq.SUB)
    self.socket.connect("tcp://localhost:%s" % port)
    self.socket.setsockopt_string(zmq.SUBSCRIBE, self.command)

  def runFeature(self):
    raise NotImplementedError
