import __future__
import collections
from functools import wraps

class ModuleProxy(collections.Mapping):
    def __init__(self):
        self._proxied_modules = {}
        self.custom_prefix = "_"

    def import_module(self, name: object) -> object:
        if isinstance(name, str):
            self._proxied_modules[name] = __future__.__builtins__["__import__"](name)
        elif isinstance(name, collections.Iterable): # assuming list or tuples here
            for item in name:
                self.import_module(item)
        else:
            raise ValueError("name should be string or a list/tuple of strings")

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
        return self._proxied_modules[key]

    def __len__(self):
        return len(self._proxied_modules)

    def __iter__(self):
        return iter(self._proxied_modules)