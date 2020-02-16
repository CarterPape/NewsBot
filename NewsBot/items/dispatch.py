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
import NewsBot.items.emailable_item
import string


class Dispatch(NewsBot.items.emailable_item.EmailableItem):
    audio_URL =         scrapy.Field()
    audio_file_path =   scrapy.Field()
    dispatched_agency = scrapy.Field()
    dispatch_date_string =  scrapy.Field()
    dispatch_datetime = scrapy.Field()
    
    @property
    def email_subject(self) -> str:
        return (
            f"New {self['dispatched_agency']} call "
            f"{self['dispatch_datetime'].strftime('%A at %l:%M %p')}"
        )
    
    @property
    def html_email_body(self) -> str:
        template_string: string.Template = self._email_template
        
        return template_string.safe_substitute({
            "email_subject":    self.email_subject,
            "dispatch_time":    self["dispatch_datetime"].strftime("%H:%M:%S"),
            "dispatch_date":    self["dispatch_datetime"].strftime("%A, %b. %e"),
            "dispatched_agency":    self["dispatched_agency"],
            "dispatch_audio_url":   self["audio_URL"],
        })
    
    @property
    def _attachment_paths(self) -> [str]:
        return [self["audio_file_path"]]
