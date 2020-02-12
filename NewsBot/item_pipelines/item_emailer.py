# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import NewsBot.items
import NewsBot.spiders
import scrapy
import scrapy.settings
import os
import string
import os.path
import magic
import requests
import keyring
import dotenv
import pape.utilities


class ItemEmailer(object):
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings = crawler.settings
        )
    
    def __init__(self, *,
        settings: scrapy.settings.Settings = None
    ):
        self._settings =    settings
        self._logger =      logging.getLogger(__name__)
        
        self._current_item:     scrapy.Item
        self._current_spider:   scrapy.spiders.Spider
        
        dotenv.load_dotenv(dotenv.find_dotenv())
        
    def process_item(
        self,
        item:   NewsBot.items.EmailableItem,
        spider: scrapy.spiders.Spider
    ) -> scrapy.Item:
        
        self._current_item =    item
        self._current_spider =  spider
        
        self._logger.info(
            requests.post(
                f"https://api.mailgun.net/v3/{os.getenv('EMAIL_SENDER_DOMAIN')}/messages",
                auth = ("api",  os.getenv("MAILGUN_API_KEY")),
                files =         self._current_item.get_email_attachments(),
                data = {
                    "from":     os.getenv("EMAIL_SENDER"),
                    "to":       os.getenv("EMAIL_RECIPIENT"),
                    "subject":  self._current_item.get_email_subject(),
                    "html":     self._current_item.get_html_email_body(),
                }
            )
        )
        return item
