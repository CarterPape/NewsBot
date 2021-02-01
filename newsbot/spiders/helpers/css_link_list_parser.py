# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import json
import logging
import urllib.parse
import typing
import scrapy.http
import newsbot.spiders.helpers.link_list_parser as link_list_parser

class CSSLinkListParser(link_list_parser.LinkListParser):
    def __init__(self, link_css: str):
        self._link_css = link_css
    
    def parse_response(self, response: scrapy.http.Response) -> typing.List[str]:
        all_urls = response.css(self._link_css).getall()
        
        return self._join_urls_with_common_base(
            common_base =   response.url,
            urls =          all_urls,
        )
