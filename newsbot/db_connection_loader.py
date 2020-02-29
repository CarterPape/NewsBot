# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.settings
import collections
import inspect
import warnings
import importlib
import pkgutil
import traceback
import newsbot.db_connections.db_connection as db_connection
import types


class DBConnectionLoader(object):
    
    def __init__(self, *,
        settings: scrapy.settings.Settings,
    ):
        self._db_connection_modules =   settings.getlist("DB_CONNECTION_MODULES")
        self._warn_only =               settings.getbool(
            "DB_CONNECTION_LOADER_WARN_ONLY",
            default = False,
        )
        self._db_connections =          list()
        self._found_classes =           collections.defaultdict(list)
        self._load_all_db_connections()
    
    def db_connection_classes(self, *,
        in_module: types.ModuleType
    ):
        module = in_module
        for _, obj in vars(module).items():
            if (
                inspect.isclass(obj)
            ) and (
                issubclass(obj, db_connection.DBConnection)
            ) and (
                obj.__module__ == module.__name__
            ) and (
                getattr(
                    obj,
                    "TABLE_NAME",
                    db_connection.DBConnection.table_definition,
                ) != db_connection.DBConnection.table_definition
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
    
    def _load_db_connections(self, *,
        from_module: types.ModuleType,
    ):
        module = from_module
        
        for db_connection_class in self.db_connection_classes(in_module = module):
            self._db_connections.append(db_connection_class)
    
    def _load_all_db_connections(self):
        for name in self._db_connection_modules:
            try:
                for module in self.walk_modules(at_path = name):
                    self._load_db_connections(from_module = module)
            except ImportError:
                if self._warn_only:
                    msg = (
                        f"\n{traceback.format_exc()}"
                        f"Could not load database connections from module '{name}'. "
                        f"See above traceback for details."
                    )
                    warnings.warn(msg, RuntimeWarning)
                else:
                    raise
    
    @classmethod
    def from_settings(cls, *,
        settings: scrapy.settings.Settings,
    ):
        return cls(settings = settings)
    
    def list(self):
        return self._db_connections
