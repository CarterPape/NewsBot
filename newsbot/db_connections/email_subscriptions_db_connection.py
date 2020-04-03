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
import pape.utilities


class EmailSubscriptionsDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "email_subscriptions"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
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
            INSERT INTO `{self.table_name}` (
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
            DELETE FROM `{self.table_name}`
            WHERE email_address = "{requester_email_address}"
        """)
        self.commit()
        db_cursor.close()
    
    def get_addressees(self, *,
        that_should_receive_item: emailable_item.EmailableItem,
    ) -> [tuple]:
        full_item_class_name = pape.utilities.full_class_name(
            of_object = that_should_receive_item
        )
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT
                addressee_name,
                email_address
            FROM `{self.table_name}`
            WHERE "{full_item_class_name}" LIKE item_selection
        """)
        addressee_list = db_cursor.fetchall()
        db_cursor.close()
        return addressee_list
    
    def get_all_subscriptions(self) -> [tuple]:
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT
                addressee_name,
                email_address,
                item_selection
            FROM `{self.table_name}`
        """)
        subscription_list = db_cursor.fetchall()
        db_cursor.close()
        return subscription_list
