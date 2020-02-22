# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import NewsBot.items.emailable_item
import NewsBot.items.emailable_item_with_attachments
import scrapy
import scrapy.settings
import os
import string
import os.path
import magic
import requests
import dotenv
import pape.utilities
import datetime


class ItemEmailer(
    NewsBot.item_pipelines.item_pipeline.ItemPipeline,
    NewsBot.logger.Logger,
):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings = crawler.settings
        )
    
    def __init__(self, *,
        settings: scrapy.settings.Settings = None
    ):
        self._settings =    settings
        
        dotenv.load_dotenv(dotenv.find_dotenv())
        
    def process_item(
        self,
        item:   NewsBot.items.emailable_item.EmailableItem,
        spider: scrapy.spiders.Spider
    ) -> scrapy.Item:
        
        if issubclass(
            type(item),
            NewsBot.items.emailable_item_with_attachments.EmailableItemWithAttachments,
        ):
            attachments = item.gather_email_attachments()
        else:
            attachments = None
        
        item["email_response"] = (
            requests.post(
                f"https://api.mailgun.net/v3/{os.getenv('EMAIL_SENDER_DOMAIN')}/messages",
                auth = ("api",  os.getenv("MAILGUN_API_KEY")),
                files =         attachments,
                data = {
                    "from":     os.getenv("EMAIL_SENDER"),
                    "to":       os.getenv("EMAIL_RECIPIENT"),
                    "subject":  item.synthesize_email_subject(),
                    "html":     item.synthesize_html_email_body(),
                }
            )
        )
        item["email_sent_datetime"] = datetime.datetime.now()
        self._logger.info(item["email_response"])
        
        return item
