# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections.abc
import scrapy.http
from newsbot.spiders.helpers import link_list_parser

class LambdaLinkListParser(link_list_parser.LinkListParser):
    def __init__(self,
        link_lambda: collections.abc.Callable[[scrapy.http.Response], list[str]],
    ):
        self._link_lambda = link_lambda
    
    def parse_response(self, response: scrapy.http.Response) -> list[str]:
        all_urls = self._link_lambda(response)
        
        return self._join_urls_with_common_base(
            common_base =   response.url,
            urls =          all_urls,
        )
