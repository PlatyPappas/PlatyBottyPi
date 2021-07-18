from pluginFramework.plugin import Plugin
import threading
from .library import lightController
from .library import colorLibrary

class lightsPlugin(Plugin):
  def __init__(self, twitchChatInstance, port):
    super().__init__(twitchChatInstance, port, "Lights Plugin", "!lights")
    self.lightController = lightController.lightController()

  def runFeature(self):
    self.lightController.colorWipe(colorLibrary.colors['purple'])
    threading.Thread(target=self.lightController.pulseBrightness, args=()).start()
    while True:
      command = self.socket.recv_string()
      parsedCommand = command.split()[1:]
      print("Command received:")
      print(parsedCommand)
      if self.validCommand(parsedCommand):
        threading.Thread(target=self.processCommand, args=(parsedCommand,)).start()
      else:
        self.twitchChatInstance.send(
            "Valid colors are: red, dark-red, blue, dark-blue, green, dark-green, purple, pink, orange, yellow, cyan, teal, peach, and white.\nAdditionally, you can name RGB values. Example: !lights 140 223 37")
  
  def validCommand(self, command):
    if len(command) == 1 and (command[0] in colorLibrary.colors):
      return True
    elif len(command) == 3 and ((int(command[0]) <= 255 and int(command[0]) >= 0) and (int(command[1]) <= 255 and int(command[1]) >= 0) and (int(command[2]) <= 255 and int(command[2]) >= 0)):
      return True
    else:
      return False
  
  def processCommand(self, command):
    if len(command) == 1:
      self.lightController.colorWipe(colorLibrary.colors[command[0]])
    else:
      self.lightController.colorWipe(colorLibrary.customColor(command))
