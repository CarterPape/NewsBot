# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import string
import os
import abc
import inspect

import scrapy.item

from newsbot.items import self_serializing_item


class EmailableItem(
    self_serializing_item.SelfSerializingItem,
    metaclass = abc.ABCMeta,
):
    email_response      =       scrapy.item.Field(ignore_when_serializing = True)
    email_sent_datetime =       scrapy.item.Field(ignore_when_serializing = True)
    
    @abc.abstractmethod
    def synthesize_email_subject(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__}.synthesize_email_subject is not defined"
        )
    
    @abc.abstractmethod
    def synthesize_html_email_body(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__}.synthesize_html_email_body is not defined"
        )
    
    def _get_email_template(self) -> string.Template:
        email_template_path = (
            os.path.abspath(
                os.path.join(
                    os.path.dirname(
                        inspect.getfile(
                            type(self)
                        )
                    ),
                    f"{type(self).__name__}.template.html",
                )
            )
        )
        
        return string.Template(
            open(
                email_template_path, "r",
                encoding = "UTF8",
            ).read()
        )
