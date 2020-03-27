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
import newsbot.items.emailable_item as emailable_item
import newsbot.items.emailable_item_with_attachments as emailable_item_with_attachments
import newsbot.item_pipelines.item_pipeline as item_pipeline
import newsbot.logger as logger


class ItemEmailer(
    item_pipeline.ItemPipeline,
    logger.Logger,
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
    
    def process_item(self,
        item:   emailable_item.EmailableItem,
        spider: scrapy.spiders.Spider,
    ) -> scrapy.Item:
        item["email_response"] = self._email_item(item)
        item["email_sent_datetime"] = datetime.datetime.now()
        self._logger.info(item["email_response"])
        
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
        
        if self._settings.getbool("_PRINT_INSTEAD_OF_EMAIL"):
            
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
            
            print("Printing emails rather than sending (check setting _PRINT_INSTEAD_OF_EMAIL)")
            print("From:", os.getenv("EMAIL_SENDER"))
            print("To:", os.getenv("EMAIL_RECIPIENTS"))
            print("Subject:", item.synthesize_email_subject())
            print("———————————\n", item.synthesize_html_email_body(), "\n- - - - - -")
            print("Attachments:\n", attachment_paths, "\n———————————\n\n")
            
            return __FakeResponse()
        
        else:
            return requests.post(
                f"https://api.mailgun.net/v3/{os.getenv('EMAIL_SENDER_DOMAIN')}/messages",
                auth = ("api",  os.getenv("MAILGUN_API_KEY")),
                files =         attachments,
                data = {
                    "from":     os.getenv("EMAIL_SENDER"),
                    "to":       os.getenv("EMAIL_RECIPIENTS"),
                    "subject":  item.synthesize_email_subject(),
                    "html":     item.synthesize_html_email_body(),
                }
            )
