import __future__

class ModuleProxy():
    def __init__(self):
        self.proxied_modules = {}

    def import_module(self, name: str) -> object:
        self.proxied_modules[name] = __future__.__builtins__["__import__"](name)