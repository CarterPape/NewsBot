# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import mysql.connector


class DBConnection(mysql.connector.MySQLConnection):
    @property
    def table_definition(self):
        raise NotImplementedError
