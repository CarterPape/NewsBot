# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot.db_connections.db_connection as db_connection
import newsbot.items.emailable_item as emailable_item
import newsbot.items.web_element as web_element
import datetime
import pytz
import typing
import difflib


class WebElementHistoryDBConnection(db_connection.DBConnection):
    TABLE_NAME =  "web_element_history"
    
    def __init__(self):
        super().__init__()
        self._current_web_element: web_element.WebElement
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.TABLE_NAME}` (
                `web_element_instance`  INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `url`                   TEXT        NOT NULL,
                `instance_content`      MEDIUMTEXT  NOT NULL,
                `first_appearance`      DATETIME    NOT NULL,
                `latest_appearance`     DATETIME    NOT NULL,
                `instance_is_current`   BOOLEAN     NOT NULL
            )
        """
    
    def record_web_element(self,
        item_to_record: web_element.WebElement
    ):
        raise NotImplementedError
        
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            INSERT INTO `{self.TABLE_NAME}` (
                send_datetime,
                status_code,
                serialized_item
            )
            VALUES (
                '{item_to_record['email_sent_datetime'].replace(tzinfo = None)}',
                {item_to_record['email_response'].status_code},
                '{item_to_record.serialized()}'
            )
        """)
        self.commit()
        db_cursor.close()
    
    def current_web_element_is_new(self) -> bool:
        raise NotImplementedError
        
        db_cursor = self.cursor(buffered = True)
        db_cursor.execute(f"""
            SELECT (
                send_datetime
            ) FROM {self.TABLE_NAME}
            WHERE
                serialized_item like '{item_to_query.serialized()}'
                AND status_code = 200
        """)
        if db_cursor.rowcount == 0:
            db_cursor.close()
            return None
        else:
            send_datetime = db_cursor.fetchone()[0]
            send_datetime = send_datetime.replace(
                tzinfo = pytz.timezone("America/Denver")
            )
            db_cursor.close()
            return send_datetime
