import zmq
import threading

class Plugin(object):

  def __init__(self, pluginSubPort, serverSubPort, description = 'UNKNOWN', command = 'UNKNOWN'):
    self.description = description
    self.command = command
    self.serviceRunning = True
    self.connectToParent(pluginSubPort, serverSubPort)

  def connectToParent(self, pluginSubPort, serverSubPort):
    pluginContext = zmq.Context()
    self.pluginSubSocket = pluginContext.socket(zmq.SUB)
    self.pluginSubSocket.connect("tcp://127.0.0.1:%s" % pluginSubPort)
    self.pluginSubSocket.setsockopt_string(zmq.SUBSCRIBE, self.command)

    serverContext = zmq.Context()
    self.serverSubSocket = serverContext.socket(zmq.REQ)
    self.serverSubSocket.bind("tcp://127.0.0.1:%s" % serverSubPort)
  
  def closeSockets(self):
    self.pluginSubSocket.close()
    self.serverSubSocket.close()
    

  def runFeature(self):
    raise NotImplementedError
