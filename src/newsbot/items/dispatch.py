# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import string

import scrapy

from newsbot.items import emailable_item_with_attachments


class Dispatch(
    emailable_item_with_attachments.EmailableItemWithAttachments,
):
    dispatched_agency =     scrapy.Field()
    datetime_dispatched =   scrapy.Field(serializer = str)
    
    def synthesize_email_subject(self) -> str:
        return (
            f"Call to {self['dispatched_agency']} "
            f"{self['datetime_dispatched'].strftime('%A at %-l:%M %p')}"
        )
    
    def synthesize_html_email_body(self) -> str:
        template_string: string.Template = self._get_email_template()
        
        return template_string.safe_substitute({
            "email_subject":    self.synthesize_email_subject(),
            "dispatch_time":    self["datetime_dispatched"].strftime("%H:%M:%S"),
            "dispatch_date":    self["datetime_dispatched"].strftime("%A, %b. %e"),
            "dispatched_agency":    self["dispatched_agency"],
            "dispatch_audio_url":   self["files"][0]["url"],
        })
