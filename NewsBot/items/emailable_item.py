# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import string
import scrapy
import os
import pape


class EmailableItem(scrapy.Item):
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
