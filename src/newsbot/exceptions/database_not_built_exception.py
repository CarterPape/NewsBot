# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections.abc

from newsbot.db_connections import db_connection

class DatabaseNotBuiltException(Exception):
    def __init__(self, *,
        db_connections_not_created: collections.abc.Iterable[db_connection.DBConnection]
    ):
        self.db_connections_not_created = db_connections_not_created
        super().__init__(self)
