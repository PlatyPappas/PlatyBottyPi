from pluginFramework.plugin import Plugin
import threading
from .library import lightController
from .library import colorLibrary

class lightsPlugin(Plugin):
  def __init__(self, twitchChatInstance, port):
    super().__init__(twitchChatInstance, port, "Lights Plugin", "!lights")
    self.lightController = lightController.lightController()

  def runFeature(self):
    threading.Thread(target=self.lightController.pulseBrightness, args=()).start()
    while True:
      command = self.socket.recv_string()
      parsedCommand = command.split()[1:]
      if self.validCommand(parsedCommand):
        threading.Thread(target=self.feature.processCommand, args=()).start()
      else:
        self.twitchChatInstance.send("Valid colors are: red, dark-red, blue, dark-blue, green, dark-green, purple, pink, orange, yellow, cyan, teal, peach, and white")
  
  def validCommand(self, command):
    if len(command) == 1 and command[0] in colorLibrary.colors:
      return True
    elif len(command) == 3 and (int(command[0]) < 255 and int(command[1]) < 255 and int(command[2]) < 255):
      return True
    else:
      return False
  
  def processCommand(self, command):
    if len(command) == 1:
      self.lightController.colorWipe(colorLibrary.colors[command])
    else:
      self.lightController.colorWipe(colorLibrary.customColor(command))
