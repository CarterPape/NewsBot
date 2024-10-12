# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import abc
import typing

import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
import scrapy.settings

class DBConnection(
    mysql.connector.MySQLConnection,
    metaclass = abc.ABCMeta
):
    def __init__(self,
        *args,
        settings: scrapy.settings.Settings,
        **kwargs,
    ):
        super().__init__(
            *args,
            database =  settings.get("_MYSQL_DATABASE"),
            user =      settings.get("_MYSQL_USER"),
            password =  settings.get("_MYSQL_PASSWORD"),
            **kwargs,
        )
    
    @property
    @abc.abstractmethod
    def table_name(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__}.table_name is not defined"
        )
    
    @property
    @abc.abstractmethod
    def table_definition(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__}.table_definition is not defined"
        )
    
    @property
    def connection_dependencies(self) -> list[type]:
        return []
    
    def table_exists(self) -> bool:
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = 'newsbot' 
            AND table_name = '{self.table_name}'
        """)
        table_count = typing.cast(list[int],
            db_cursor.fetchone()
        )[0]
        db_cursor.close()
        
        exists_or_not = (
            "exists"
                if table_count > 0
            else "does not exist"
        )
        logging.debug(f"Table {self.table_name} {exists_or_not}")
        
        return table_count > 0
    
    def create_table(self):
        logging.info(f"Creating table {self.table_name}")
        
        db_cursor = self.cursor()
        db_cursor.execute(self.table_definition)
        self.commit()
        db_cursor.close()
    
    def commit(self):
        logging.debug(f"Committing transaction on table {self.table_name}")
        super().commit()
