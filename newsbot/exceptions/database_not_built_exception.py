# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot.db_connections.db_connection as db_connection
import typing

class DatabaseNotBuiltException(Exception):
    def __init__(self, *,
        db_connections_not_created: typing.Iterable[db_connection.DBConnection]
    ):
        self.db_connections_not_created = db_connections_not_created
