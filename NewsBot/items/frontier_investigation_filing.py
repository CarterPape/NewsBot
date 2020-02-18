# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import NewsBot.items.emailable_item
import NewsBot.items.dated_item
import NewsBot.items.item_with_files
import string


class FrontierInvestigationFiling(
    NewsBot.items.emailable_item.EmailableItem,
    NewsBot.items.dated_item.DatedItem,
    NewsBot.items.item_with_files.ItemWithFiles,
):
    audio_URL =         scrapy.Field()
    audio_file_path =   scrapy.Field()
    dispatched_agency = scrapy.Field()
    
    @property
    def email_subject(self) -> str:
        return (
            f"Call to {self['dispatched_agency']} "
            f"{self['datetime'].strftime('%A at %l:%M %p')}"
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
