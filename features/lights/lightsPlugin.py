from pluginFramework.plugin import Plugin
import zmq
import json
from .library import colorLibrary

class lightsPlugin(Plugin):
  def __init__(self, pluginSubPort, serverSubPort):
    super().__init__(pluginSubPort, serverSubPort, "Lights Plugin", "!lights")
    self.interfaceContext = zmq.Context()
    self.interfaceSocket = self.interfaceContext.socket(zmq.REQ)
    self.interfaceSocket.connect("tcp://10.0.0.231:%s" % "2555")

    modeContext = zmq.Context()
    modeSocket = modeContext.socket(zmq.REQ)
    modeSocket.connect("tcp://10.0.0.231:%s" % "2556")
    modeSocket.send_string("WIPE")
    modeSocket.recv_string()
    modeSocket.close()

  def runFeature(self):
    while self.serviceRunning:
      command = self.pluginSubSocket.recv_string()
      parsedCommand = command.split()[1:]
      if parsedCommand:
        print("Command received: " + command)
      if self.validCommand(parsedCommand):
        print("Command valid")
        self.processCommand(parsedCommand)
      else:
        separator = ' '
        recombinedCommand = separator.join(parsedCommand)
        messToPack = "For color options, type: !lights options. For instructions, type: !light help"
        if recombinedCommand:
          if recombinedCommand.lower() == "options" or recombinedCommand.lower() == "option":
            tempMess = "Color options available: "
            for key in colorLibrary.colors:
              tempMess += key
              tempMess += ", "
            messToPack = tempMess[:-2]
          elif recombinedCommand.lower() == "help":
            messToPack = "For color options, type: !lights options. Alternatively, you can name RGB values. Example: !lights 140 223 37"
          else:
            print("Command invalid")
        else:
          print("Command invalid")
        
        messToSend = {"message": messToPack}
        jsonMess = json.dumps(messToSend)
        self.serverSubSocket.send_json(jsonMess)
        self.serverSubSocket.recv_string()
    self.closeSockets()
  
  def validCommand(self, command):
    if len(command) == 1 and (command[0] in colorLibrary.colors):
      return True
    elif len(command) == 3:
      if command[0].isdigit() and command[1].isdigit() and command[2].isdigit():
        if ((int(command[0]) <= 255 and int(command[0]) >= 0) and (int(command[1]) <= 255 and int(command[1]) >= 0) and (int(command[2]) <= 255 and int(command[2]) >= 0)):
          return True
        else:
          return False
      else:
        return False
    else:
      return False
  
  def processCommand(self, command):
    if len(command) == 1:
      self.interfaceSocket.send_string(colorLibrary.colors[command[0]])
    else:
      separator = ' '
      self.interfaceSocket.send_string(separator.join(command))
    reply = self.interfaceSocket.recv_string()
    print(reply)
