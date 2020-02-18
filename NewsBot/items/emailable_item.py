# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import string
import scrapy.item
import NewsBot.items.self_serializing_item
import os


class EmailableItem(NewsBot.items.self_serializing_item.SelfSerializingItem):
    email_response = scrapy.item.Field(ignore_when_serializing = True)
    
    @property
    def email_subject(self) -> str:
        raise NotImplementedError
    
    @property
    def html_email_body(self) -> str:
        raise NotImplementedError
    
    @property
    def _email_template(self) -> string.Template:
        email_template_path = (
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    f"{type(self).__name__}.template.html",
                )
            )
        )
        
        return string.Template(open(email_template_path, "r").read())
