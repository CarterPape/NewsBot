# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import pytz
import typing
import newsbot.db_connections.db_connection as db_connection
import newsbot.items.emailable_item as emailable_item


class EmailSubscriptionsDBConnection(db_connection.DBConnection):
    TABLE_NAME =  "email_subscriptions"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.TABLE_NAME}` (
                `subscription_id`           INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `addressee_name`            TEXT,
                `email_address`             TINYTEXT    NOT NULL,
                `item_selection`            TEXT        NOT NULL
            )
        """
    
    def add_subscription(self, *,
        addressee_name: str = None,
        email_address: str,
        item_selection: str,
    ):
        addressee_name_with_quotes_or_null = f"\"{addressee_name}\"" or "NULL"
        
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            INSERT INTO `{self.TABLE_NAME}` (
                addressee_name,
                email_address,
                item_selection
            )
            VALUES (
                {addressee_name_with_quotes_or_null},
                "{email_address}",
                "{item_selection}"
            )
        """)
        self.commit()
        db_cursor.close()
    
    def remove_all_subscriptions(self, *,
        requester_email_address: str
    ):
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            DELETE FROM `{self.TABLE_NAME}`
            WHERE email_address = "{requester_email_address}"
        """)
        self.commit()
        db_cursor.close()
    
    def get_addressees(self, *,
        subscribed_to_items_named: str,
    ) -> [str]:
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT (
                addressee_name,
                email_address
            )
            FROM {self.TABLE_NAME}
            WHERE "{subscribed_to_items_named}" LIKE item_selection
        """)
        addressee_list = db_cursor.fetchall()
        db_cursor.close()
        return [
            (
                f"{addressee[0]} <{addressee[1]}>"
                if addressee[0] == None
                else f"{addressee[1]}"
            )
            for addressee
            in addressee_list
        ]
