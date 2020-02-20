# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
import dotenv
import os
import time

class DBConnection(mysql.connector.MySQLConnection):
    def __init__(self, *args, **kwargs):
        dotenv.load_dotenv(dotenv.find_dotenv())
        
        super().__init__(
            database =  os.getenv("MYSQL_DATABASE"),
            user =      os.getenv("MYSQL_USER"),
            password =  os.getenv("MYSQL_PASSWORD"),
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
