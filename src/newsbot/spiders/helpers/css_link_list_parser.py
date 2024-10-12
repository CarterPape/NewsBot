# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

from newsbot.spiders.helpers import lambda_link_list_parser

class CSSLinkListParser(lambda_link_list_parser.LambdaLinkListParser):
    def __init__(self, link_css: str):
        super().__init__(
            lambda response: response.css(link_css).getall()
        )
