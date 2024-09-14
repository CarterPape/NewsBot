# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging

import scrapy
import scrapy.settings

from newsbot.db_connections import db_connection
from newsbot import concrete_subclass_loader
from newsbot.exceptions import database_not_built_exception


class DBBuilder:
    def __init__(self, *,
        from_settings: scrapy.settings.Settings,
    ):
        self._settings = from_settings
        
        self._db_connection_loader = concrete_subclass_loader.ConcreteSubclassLoader(
            load_subclasses_of =    db_connection.DBConnection,
            from_modules_named =    self._settings.getlist("_TOP_LEVEL_MODULES"),
        )
        
        self._principal_db_connection_list = set(
            db_connection_class(settings = self._settings)
            for db_connection_class
            in self._db_connection_loader.list()
        )
        
        self._currently_building:       set
        self._deferred_for_building:    set
    
    def build_unbuilt_tables(self):
        logging.debug("Building all unbuilt database tables")
        self._currently_building =      self._principal_db_connection_list
        
        while (
            self._currently_building
        ) and (
            len(self._currently_building) > 0
        ):
            self._deferred_for_building = set()
            self._maybe_build_current_set()
            self._currently_building = self._deferred_for_building
        
        for each_db_connection in self._principal_db_connection_list:
            each_db_connection.close()
    
    def _maybe_build_current_set(self):
        for each_db_connection in self._currently_building:
            if each_db_connection.table_exists():
                logging.debug(f"Table {each_db_connection.table_name} already built")
            else:
                self._build_or_defer(each_db_connection)
        
        if self._currently_building == self._deferred_for_building:
            raise database_not_built_exception.DatabaseNotBuiltException(
                db_connections_not_created = self._deferred_for_building,
            )
    
    def _build_or_defer(self, the_db_connection: db_connection.DBConnection):
        if self._dependencies_for_db_connection_exist(the_db_connection):
            logging.debug(f"Building table {the_db_connection.table_name}")
            the_db_connection.create_table()
        else:
            logging.debug(
                f"Deferring table {the_db_connection.table_name} construction "
                "because at least one of its dependencies is unbuilt"
            )
            self._deferred_for_building.add(the_db_connection)
    
    def _dependencies_for_db_connection_exist(self, the_db_connection: db_connection.DBConnection):
        all_exist = True
        
        for each_dependency in the_db_connection.connection_dependencies:
            logging.debug(f"Dependency for {the_db_connection} found: {each_dependency}")
            all_exist = (
                all_exist
            ) and (
                each_dependency(
                    settings = self._settings
                ).table_exists()
            )
        
        return all_exist
