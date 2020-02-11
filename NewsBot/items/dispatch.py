# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from NewsBot.items.emailable_item import EmailableItem
import string


class Dispatch(EmailableItem):
    audio_URL =         scrapy.Field()
    audio_file_path =   scrapy.Field()
    dispatched_agency = scrapy.Field()
    dispatch_date_string =  scrapy.Field()
    dispatch_datetime = scrapy.Field()
    
    def get_email_subject(self) -> str:
        return (
            f"New {self['dispatched_agency']} call "
            f"{self['dispatch_datetime'].strftime('%A at %l:%M %p')}"
        )
    
    def get_html_email_body(self) -> str:
        template_string: string.Template = self._get_email_template(from_item_file_path = __file__)
        
        return template_string.safe_substitute({
            "email_subject":    self.get_email_subject(),
            "dispatch_time":    self["dispatch_datetime"].strftime("%H:%M:%S"),
            "dispatch_date":    self["dispatch_datetime"].strftime("%A, %b. %e"),
            "dispatched_agency":    self["dispatched_agency"],
            "dispatch_audio_url":   self["audio_URL"],
        })
    
    def _get_attachment_paths(self) -> [str]:
        return [self["audio_file_path"]]
