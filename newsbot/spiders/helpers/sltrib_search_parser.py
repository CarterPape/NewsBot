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

class SLTribSearchParser(link_list_parser.LinkListParser):
    def __init__(self):
        self._search_content_xpath = "//*[@title='Search Results']/@content"
    
    def parse_response(self, response: scrapy.http.Response) -> typing.List[str]:
        search_content = response.xpath(self._search_content_xpath).get()
        search_result_list = json\
            .loads(search_content)\
            ["content_elements"]
        
        return [
            urllib.parse.urljoin(
                response.url,
                each_result["website_url"],
            )
            for each_result
            in search_result_list
        ]
