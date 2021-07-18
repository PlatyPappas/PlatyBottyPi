import os
import pkgutil
import inspect
from pluginFramework.plugin import Plugin

class PluginCollection(object):

  def __init__(self, features):
    self.features = features
    self.load_plugins()
  
  def load_plugins(self):
    self.plugins = []
    self.seen_paths = []
    self.walk_package(self.features)

  def walk_package(self, package):
      imported_package = __import__(package, fromlist=['blah'])

      for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not ispkg:
          plugin_module = __import__(pluginname, fromlist=['blah'])
          clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
          for (_, c) in clsmembers:
            if issubclass(c, Plugin) & (c is not Plugin):
              print(f'Found plugin class: {c.__module__}.{c.__name__}')
              self.plugins.append(c)

      all_current_paths = []
      if isinstance(imported_package.__path__, str):
        all_current_paths.append(imported_package.__path__)
      else:
        all_current_paths.extend([x for x in imported_package.__path__])

      for pkg_path in all_current_paths:
        if pkg_path not in self.seen_paths:
          self.seen_paths.append(pkg_path)

          child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

          for child_pkg in child_pkgs:
            self.walk_package(package + '.' + child_pkg)
