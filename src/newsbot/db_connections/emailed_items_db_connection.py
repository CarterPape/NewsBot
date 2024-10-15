# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import logging

import zoneinfo

from newsbot.db_connections import db_connection
from newsbot.items import emailable_item


class EmailedItemsDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "sent_emails"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `email_no`          INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `send_datetime`     DATETIME    NOT NULL,
                `status_code`       SMALLINT    NOT NULL,
                `serialized_item`   MEDIUMTEXT  NOT NULL
            )
        """
    
    def record_emailed_item(self,
        item_to_record: emailable_item.EmailableItem
    ):
        logging.debug(f"Recording item {item_to_record} as emailed")
        
        db_cursor = self.cursor()
        db_cursor.execute(
            f"""
                INSERT INTO `{self.table_name}` (
                    send_datetime,
                    status_code,
                    serialized_item
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
            """,
            (
                item_to_record["email_sent_datetime"].replace(tzinfo = None),
                item_to_record["email_response"].status_code,
                item_to_record.serialized(),
            )
        )
        self.commit()
        db_cursor.close()
    
    def datetime_item_transmitted(self,
        item_to_query: emailable_item.EmailableItem
    ) -> (datetime.datetime | None):
        
        logging.debug(f"Getting datetime of transmission (if one exists) for item {item_to_query}")
        
        db_cursor = self.cursor(buffered = True)
        db_cursor.execute(
            f"""
                SELECT
                    send_datetime
                FROM {self.table_name}
                WHERE
                    serialized_item = %s
                    AND status_code = 200
            """,
            (
                item_to_query.serialized(),
            ),
        )
        if db_cursor.rowcount == 0:
            db_cursor.close()
            return None
        else:
            the_row = db_cursor.fetchone()
            assert isinstance(the_row, tuple)
            
            send_datetime = the_row[0]
            assert isinstance(send_datetime, datetime.datetime)
            
            send_datetime = send_datetime.replace(
                tzinfo = zoneinfo.ZoneInfo("America/Denver")
            )
            db_cursor.close()
            return send_datetime
