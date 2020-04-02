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
import abc


class EmailableItem(
    self_serializing_item.SelfSerializingItem,
    metaclass = abc.ABCMeta,
):
    email_response      =       scrapy.item.Field(ignore_when_serializing = True)
    email_sent_datetime =       scrapy.item.Field(ignore_when_serializing = True)
    
    @abc.abstractmethod
    def synthesize_email_subject(self) -> str:
        pass
    
    @abc.abstractmethod
    def synthesize_html_email_body(self) -> str:
        pass
    
    def _get_email_template_directory(self):
        return os.path.dirname(__file__)
    
    def _get_email_template(self) -> string.Template:
        email_template_path = (
            os.path.abspath(
                os.path.join(
                    self._get_email_template_directory(),
                    f"{type(self).__name__}.template.html",
                )
            )
        )
        
        return string.Template(open(email_template_path, "r").read())
