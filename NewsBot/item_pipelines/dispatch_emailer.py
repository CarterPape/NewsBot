# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import NewsBot.items
import NewsBot.spiders
import scrapy.settings
import os
import string
import os.path
import magic
import requests
import keyring
import dotenv


class DispatchEmailer(object):
    
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
        self.mail_sender =  scrapy.mail.MailSender.from_settings(self._settings)
        
        self._current_item:     NewsBot.items.Dispatch
        self._current_spider:   NewsBot.spiders.DispatchCallLogSpider
        
        self._email_template_path = \
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "email.template.html",
                )
            )
        self._email_body: string.Template
        
        dotenv.load_dotenv(dotenv.find_dotenv())
        
    def process_item(
        self,
        item: NewsBot.items.Dispatch,
        spider: NewsBot.spiders.DispatchCallLogSpider
    ) -> NewsBot.items.Dispatch:
        
        self._current_item =    item
        self._current_spider =  spider
        
        self._logger.info(
            requests.post(
                f"https://api.mailgun.net/v3/{os.getenv('EMAIL_SENDER_DOMAIN')}/messages",
                auth = ("api", keyring.get_password(
                    service_name =  "api.mailgun.net",
                    username =      os.getenv("MAILGUN_API_USER"),
                )),
                files = [
                    ("attachment", (
                        os.path.basename(self._current_item["audio_file_path"]),
                        open(self._current_item["audio_file_path"], "rb").read()
                    )),
                ],
                data = {
                    "from": os.getenv("EMAIL_SENDER"),
                    "to": os.getenv("EMAIL_RECIPIENT"),
                    "subject": self._get_email_subject(),
                    "html": self._get_email_body(),
                }
            )
        )
        return item
    
    def _get_email_subject(self):
        return f"New {self._current_item['dispatched_agency']} call " \
            f"{self._current_item['dispatch_datetime'].strftime('%A at %l:%M %p')}"
    
    def _get_email_body(self):
        with open(self._email_template_path) as template_file:
            self._email_body = string.Template(template_file.read())
        return self._email_body.safe_substitute({
            "email_subject":    self._get_email_subject(),
            "dispatch_time":    self._current_item["dispatch_datetime"].strftime("%H:%M:%S"),
            "dispatch_date":    self._current_item["dispatch_datetime"].strftime("%A, %b. %e"),
            "dispatched_agency":    self._current_item["dispatched_agency"],
            "dispatch_audio_url":   self._current_item["audio_URL"],
        })
