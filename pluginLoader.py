from pluginFramework.pluginCollection import PluginCollection
from dotenv import load_dotenv
import threading
import os
import signal
import zmq

if __name__ == '__main__':
  plugins = PluginCollection('features')
  load_dotenv()
  pluginSubPort = os.environ.get("pluginSubPort")
  serverSubPort = os.environ.get("serverSubPort")
  int(pluginSubPort)
  int(serverSubPort)

  pluginThreads = []
  features = []

  for plugin in plugins.plugins:
    feature = plugin(pluginSubPort, serverSubPort)
    features.append(feature)
    pluginThreads.append(threading.Thread(target=feature.runFeature, args=()))
  for plugin in pluginThreads:
    plugin.start()

  #Closure so we can have all of the threads and plugins available
  def cleanUpThreads(*args):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:%s" % pluginSubPort)

    for feature in features:
      feature.serviceRunning = False
      socket.send_string(feature.command)

    for pluginThread in pluginThreads:
      pluginThread.join()

  signal.signal(signal.SIGINT, cleanUpThreads)
  while True:
    pass
