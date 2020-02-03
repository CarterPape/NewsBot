# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import NewsBot.items
import NewsBot.spiders
import NewsBot.item_pipelines
import scrapy.mail
import scrapy.settings
import environment
import string
import os.path
import magic
import requests
import keyring

class DispatchEmailer(object):
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings = crawler.settings
        )
    
    def __init__(self, *,
        settings: scrapy.settings.Settings = None
    ):
        self._settings      = settings
        self._logger        = logging.getLogger(__name__)
        self.mail_sender    = scrapy.mail.MailSender.from_settings(self._settings)
        
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
        
    def process_item(
        self,
        item: NewsBot.items.Dispatch,
        spider: NewsBot.spiders.DispatchCallLogSpider
    ) -> NewsBot.items.Dispatch:
        
        self._current_item      = item
        self._current_spider    = spider
        
        self._logger.info(
            requests.post(
                f"https://api.mailgun.net/v3/{environment.EMAIL_SENDER_DOMAIN}/messages",
                auth = ("api", keyring.get_password(
                    service_name    = environment.EMAIL_SERVICE_NAME,
                    username        = environment.API_USER,
                )),
                files = [
                    ("attachment", (
                        os.path.basename(self._current_item["audio_file_path"]),
                        open(self._current_item["audio_file_path"], "rb").read()
                    )),
                ],
                data = {
                    "from": environment.EMAIL_SENDER,
                    "to": environment.EMAIL_RECIPIENT,
                    "subject": self._get_email_subject(),
                    "html": self._get_email_body(),
                }
            )
        )
        return item
    
    def _get_email_subject(self):
        return f"New {self._current_item['dispatched_agency']} call " \
            f"at {self._current_item['dispatch_datetime'].strftime('%l:%M %p')}"
    
    def _get_email_body(self):
        with open(self._email_template_path) as template_file:
            self._email_body = string.Template(template_file.read())
        return self._email_body.safe_substitute({
            "email_subject":    self._get_email_subject(),
            "dispatch_time":    self._current_item["dispatch_datetime"].strftime("%H:%M:%S"),
            "dispatch_date":    self._current_item["dispatch_datetime"].strftime("%b. %d"),
            "dispatched_agency":    self._current_item["dispatched_agency"],
            "dispatch_audio_url":   self._current_item["audio_URL"],
        })
