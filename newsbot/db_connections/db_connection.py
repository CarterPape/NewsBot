# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.settings
import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
import dotenv
import os

class DBConnection(mysql.connector.MySQLConnection):
    def __init__(self, *args, settings: scrapy.settings.Settings, **kwargs):
        super().__init__(
            database =  settings.get("_MYSQL_DATABASE"),
            user =      settings.get("_MYSQL_USER"),
            password =  settings.get("_MYSQL_PASSWORD"),
            *args,
            **kwargs,
        )
    
    @property
    def table_definition(self):
        raise NotImplementedError
    
    def table_exists(self):
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = 'newsbot' 
            AND table_name = '{self.TABLE_NAME}'
        """)
        table_count = db_cursor.fetchone()[0]
        db_cursor.close()
        return table_count > 0
    
    def create_table(self):
        db_cursor = self.cursor()
        db_cursor.execute(self.table_definition)
        db_cursor.close()
