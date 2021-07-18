from pluginFramework.plugin import Plugin

class lightsPlugin(Plugin):
  def __init__(self, twitchChatInstance, port):
    super().__init__(twitchChatInstance, port, "Lights Plugin", "!lights")

  def featureHandler(self, command):
    print(command)
