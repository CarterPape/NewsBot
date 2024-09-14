# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import logging

import pape.utilities

from newsbot.db_connections import db_connection
from newsbot.items import emailable_item


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
        addressee_name: str | None = None,
        email_address: str,
        item_selection: str,
    ):
        addressee_name_with_quotes_or_null = (
            f"\"{addressee_name}\""
            if addressee_name
            else "NULL"
        )
        
        logging.info(
            f"Adding subscription to {item_selection} for \"{addressee_name}\" <{email_address}>"
        )
        
        db_cursor = self.cursor()
        db_cursor.execute(
            f"""
                INSERT INTO `{self.table_name}` (
                    addressee_name,
                    email_address,
                    item_selection
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
            """,
            (
                addressee_name_with_quotes_or_null,
                email_address,
                item_selection
            )
        )
        self.commit()
        db_cursor.close()
    
    def remove_all_subscriptions(self, *,
        requester_email_address: str
    ):
        logging.info(f"Removing all subscriptions for {requester_email_address}")
        
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            DELETE FROM `{self.table_name}`
            WHERE email_address = "{requester_email_address}"
        """)
        self.commit()
        db_cursor.close()
    
    def get_addressees_that_should_receive(self,
        item: emailable_item.EmailableItem,
    ) -> typing.List[tuple]:
        full_item_class_name = pape.utilities.full_class_name(
            of_object = item
        )
        logging.debug(f"Getting subscriptions for item of class {full_item_class_name}")
        db_cursor = self.cursor()
        db_cursor.execute(
            f"""
                SELECT
                    addressee_name,
                    email_address
                FROM `{self.table_name}`
                WHERE %s LIKE item_selection
            """,
            (
                full_item_class_name,
            )
        )
        addressee_list = db_cursor.fetchall()
        db_cursor.close()
        return addressee_list
    
    def get_all_subscriptions(self) -> typing.List[tuple]:
        logging.debug("Getting all subscriptions")
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
