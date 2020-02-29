# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import string
import scrapy.item
import newsbot.items.self_serializing_item as self_serializing_item
import os


class EmailableItem(self_serializing_item.SelfSerializingItem):
    email_response      = scrapy.item.Field(ignore_when_serializing = True)
    email_sent_datetime = scrapy.item.Field(ignore_when_serializing = True)
    
    def synthesize_email_subject(self) -> str:
        raise NotImplementedError
    
    def synthesize_html_email_body(self) -> str:
        raise NotImplementedError
    
    def _get_email_template(self) -> string.Template:
        email_template_path = (
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    f"{type(self).__name__}.template.html",
                )
            )
        )
        
        return string.Template(open(email_template_path, "r").read())
