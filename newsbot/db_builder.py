# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import newsbot.db_connections.db_connection as db_connection
import newsbot.concrete_subclass_loader as concrete_subclass_loader
import scrapy
import newsbot.exceptions.database_not_built_exception as database_not_built_exception


class DBBuilder(object):
    def __init__(self, *,
        from_settings: scrapy.settings.Settings,
    ):
        project_settings = from_settings
        
        self._db_connection_loader = concrete_subclass_loader.ConcreteSubclassLoader(
            load_subclasses_of =    db_connection.DBConnection,
            from_modules_named =    project_settings.getlist("_TOP_LEVEL_MODULES"),
        )
        
        self._principal_db_connection_list = set([
            db_connection_class(settings = project_settings)
            for db_connection_class
            in self._db_connection_loader.list()
        ])
        
        self._currently_building:       set
        self._deferred_for_building:    set
    
    def build_all_db_connections(self):
        self._currently_building =      self._principal_db_connection_list
        
        while (
            self._currently_building
        ) and (
            len(self._currently_building) > 0
        ):
            self._deferred_for_building = set()
            self._maybe_build_current_set()
            self._currently_building = self._deferred_for_building
        
        for db_connection in self._principal_db_connection_list:
            db_connection.close()
    
    def _maybe_build_current_set(self):
        for db_connection in self._currently_building:
            if db_connection.table_exists():
                pass
            else:
                self._build_or_defer(db_connection)
        
        if self._currently_building == self._deferred_for_building:
            raise database_not_built_exception.DatabaseNotBuiltException(
                db_connections_not_created = self._deferred_for_building,
            )
    
    def _build_or_defer(self, db_connection: db_connection.DBConnection):
        if self._dependencies_for_db_connection_exist(db_connection):
            db_connection.create_table()
        else:
            self._deferred_for_building.add(db_connection)
    
    def _dependencies_for_db_connection_exist(self, db_connection: db_connection.DBConnection):
        all_exist = True
        
        for each_dependency in db_connection.connection_dependencies:
            all_exist = all_exist and each_dependency.table_exists()
        
        return all_exist
