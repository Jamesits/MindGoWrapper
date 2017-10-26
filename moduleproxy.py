import __future__
import collections

class ModuleProxy():
    def __init__(self):
        self.proxied_modules = {}

    def import_module(self, name: object) -> object:
        if isinstance(name, str):
            self.proxied_modules[name] = __future__.__builtins__["__import__"](name)
        elif isinstance(name, collections.Iterable): # assuming list or tuples here
            for item in name:
                self.import_module(item)
        else:
            raise ValueError("name should be string or a list/tuple of strings")