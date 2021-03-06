# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.settings
import os
import requests
import dotenv
import datetime
import logging
import newsbot.db_connections.email_subscriptions_db_connection as email_subscriptions_db_connection
import newsbot.items.emailable_item as emailable_item
import newsbot.items.emailable_item_with_attachments as emailable_item_with_attachments
import newsbot.item_pipelines.item_pipeline as item_pipeline


class ItemEmailer(item_pipeline.ItemPipeline):
    def __init__(self):
        self._settings: scrapy.settings.Settings
    
    def process_item(self,
        item:   emailable_item.EmailableItem,
        spider: scrapy.spiders.Spider,
    ) -> scrapy.Item:
        
        logging.debug(f"Processing item {item} from spider {spider}")
        self._settings = spider.settings
        item["email_response"] = self._email_item(item)
        item["email_sent_datetime"] = datetime.datetime.now()
        
        return item
    
    def _email_item(self,
        item: emailable_item.EmailableItem,
    ):
        if issubclass(
            type(item),
            emailable_item_with_attachments.EmailableItemWithAttachments,
        ):
            attachments = item.gather_email_attachments()
        else:
            attachments = None
        
        db_connection = (
            email_subscriptions_db_connection.EmailSubscriptionsDBConnection(
                settings = self._settings
            )
        )
        
        addressee_list = db_connection.get_addressees_that_should_receive(item)
        formatted_addressee_list = [
            (
                f"{addressee[0]} <{addressee[1]}>"
                if addressee[0] != None
                else f"{addressee[1]}"
            )
            for addressee
            in addressee_list
        ]
        
        if self._settings.getbool("_PRINT_INSTEAD_OF_EMAIL"):
            
            logging.warning("Logging email at level INFO rather than sending them (check setting _PRINT_INSTEAD_OF_EMAIL)")
            class __FakeResponse(requests.Response):
                @property
                def status_code(self) -> int:
                    return 200
                    
                @status_code.setter
                def status_code(self, new_value):
                    pass
                
                @status_code.deleter
                def status_code(self):
                    pass
            
            attachment_paths = "\n".join([
                f"    {attachment[1][0]}"
                for attachment in attachments
            ])
            
            faux_email_message = (
                "From:"
                    + self._settings.get("_EMAIL_SENDER") + "\n"
                + "To:"
                    + ", ".join(formatted_addressee_list) + "\n"
                + "Subject:"
                    + item.synthesize_email_subject() + "\n"
                + "———————————\n"
                + item.synthesize_html_email_body() + "\n"
                + "- - - - - -\n"
                + "Attachments:\n"
                + attachment_paths + "\n"
                + "———————————\n\n"
            )
            
            logging.info("Email intentionally not sent:\n" + faux_email_message)
            return __FakeResponse()
        
        else:
            response = requests.post(
                f"https://api.mailgun.net/v3/{self._settings.get('_EMAIL_SENDER_DOMAIN')}/messages",
                auth = ("api",  self._settings.get("_MAILGUN_API_KEY")),
                files =         attachments,
                data = {
                    "from":     self._settings.get("_EMAIL_SENDER"),
                    "to":       ", ".join(formatted_addressee_list),
                    "subject":  item.synthesize_email_subject(),
                    "html":     item.synthesize_html_email_body(),
                }
            )
            
            logging.debug(f"Email attempt yielded {response}")
            return response
