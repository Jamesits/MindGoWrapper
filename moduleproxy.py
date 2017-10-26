import __future__
import collections
from functools import wraps

class ModuleProxy(collections.Mapping):
    def __init__(self):
        self._proxied_modules = {}
        self.custom_prefix = "_"

    def _import_module(self, name: str):
        """The magic happens here"""
        self._proxied_modules[name] = __future__.__builtins__["__import__"](name)

    def import_module(self, *args):
        """Import modules recursively"""
        for item in args:
            if isinstance(name, str):
                self._import_module(item)
            elif isinstance(name, collections.Iterable):
                self.import_module(item)
            else:
                raise KeyError("I don't know what to import since this is a " + str(item))

    def imported(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, module in self._proxied_modules.items():
                if name not in func.__globals__: # only executed once
                    func.__globals__[name] = module
                    func.__globals__[self.custom_prefix + name] = module # workaround on string match
            return func(*args, **kwargs)
        return wrapper

    def __getitem__(self, key):
        try: 
            return self._proxied_modules[key]
        except KeyError:
            if key.startswith(self.custom_prefix):
                key = key[len(self.custom_prefix):]
            return self._proxied_modules[key]

    def __len__(self):
        return len(self._proxied_modules)

    def __iter__(self):
        return iter(self._proxied_modules)