# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import NewsBot.db_connections.db_connection as db_connection


class EmailedItemsDBConnection(db_connection.DBConnection):
    name =  __name__
    
    @property
    def table_definition(self):
        return """
            CREATE TABLE `sent_emails` (
                `email_no`          INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `send_datetime`     DATETIME    NOT NULL,
                `status_code`       SMALLINT    NOT NULL,
                `subject`           TEXT        NOT NULL,
                `serialized_item`   JSON        NOT NULL
            )
        """
