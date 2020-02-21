# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import NewsBot.items.emailable_item_with_attachments
import NewsBot.items.dated_item
import NewsBot.items.self_serializing_item
import string


class Dispatch(
    NewsBot.items.emailable_item_with_attachments.EmailableItemWithAttachments,
    NewsBot.items.dated_item.DatedItem,
):
    dispatched_agency = scrapy.Field()
    
    def synthesize_email_subject(self) -> str:
        return (
            f"Call to {self['dispatched_agency']} "
            f"{self['datetime'].strftime('%A at %l:%M %p')}"
        )
    
    def synthesize_html_email_body(self) -> str:
        template_string: string.Template = self._get_email_template()
        
        return template_string.safe_substitute({
            "email_subject":    self.synthesize_email_subject(),
            "dispatch_time":    self["datetime"].strftime("%H:%M:%S"),
            "dispatch_date":    self["datetime"].strftime("%A, %b. %e"),
            "dispatched_agency":    self["dispatched_agency"],
            "dispatch_audio_url":   self["files"][0]["url"],
        })
