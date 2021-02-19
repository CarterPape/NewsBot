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

class LambdaLinkListParser(link_list_parser.LinkListParser):
    def __init__(self,
        link_lambda: typing.Callable[[scrapy.http.Response], typing.List[str]],
    ):
        self._link_lambda = link_lambda
    
    def parse_response(self, response: scrapy.http.Response) -> typing.List[str]:
        all_urls = self._link_lambda(response)
        
        return self._join_urls_with_common_base(
            common_base =   response.url,
            urls =          all_urls,
        )
