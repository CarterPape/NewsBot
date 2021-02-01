# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections
import inspect
import logging
import importlib
import pkgutil
import types

class ConcreteSubclassLoader(object):
    def __init__(self, *,
        load_subclasses_of: type,
        from_modules_named: [str],
    ):
        self._load_subclasses_of =      load_subclasses_of
        self._from_modules_named =      from_modules_named
        self._found_classes =           collections.defaultdict(list)
        self._loaded_concrete_subclasses =  list()
        
        self._load_all_subclasses()
    
    def concrete_subclasses(self, *,
        in_module: types.ModuleType
    ):
        module = in_module
        for _, obj in vars(module).items():
            if (
                inspect.isclass(obj)
            ) and (
                issubclass(obj, self._load_subclasses_of)
            ) and (
                obj.__module__ == module.__name__
            ) and (
                not inspect.isabstract(obj)
            ):
                yield obj
    
    def walk_modules(self, *,
        at_path: str,
    ) -> [types.ModuleType]:
        path =  at_path
        mods =  []
        mod =   importlib.import_module(path)
        mods.append(mod)
        if hasattr(mod, "__path__"):
            for _, subpath, is_package in pkgutil.iter_modules(mod.__path__):
                fullpath = path + "." + subpath
                if is_package:
                    mods += self.walk_modules(at_path = fullpath)
                else:
                    submod = importlib.import_module(fullpath)
                    mods.append(submod)
        
        return mods
    
    def _load_subclasses(self, *,
        from_module: types.ModuleType,
    ):
        module = from_module
        logging.debug(f"Searching for subclasses of {self._load_subclasses_of} in module {module}")
        
        for concrete_subclass in self.concrete_subclasses(in_module = module):
            logging.debug(f"Found {concrete_subclass}, a concrete subclass of {self._load_subclasses_of}")
            self._loaded_concrete_subclasses.append(concrete_subclass)
    
    def _load_all_subclasses(self):
        logging.debug(f"Loading sublasses of {self._load_subclasses_of}")
        
        for name in self._from_modules_named:
            logging.debug(f"Searching for subclasses of {self._load_subclasses_of} in name {name}")
            
            for module in self.walk_modules(at_path = name):
                self._load_subclasses(from_module = module)
    
    def list(self):
        return self._loaded_concrete_subclasses
