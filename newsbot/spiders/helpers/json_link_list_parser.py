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
import scrapy
import newsbot.spiders.helpers.link_list_parser as link_list_parser

class JSONLinkListParser(link_list_parser.LinkListParser):
    def __init__(self, *,
        json_extractor: typing.Callable[[scrapy.http.Response], str] = (
            lambda response: response.text
        ),
        item_list_selector: typing.Callable[[object], typing.List[object]],
        item_url_selector:  typing.Callable[[object], str],
    ):
        self._json_extractor = json_extractor
        self._item_list_selector = item_list_selector
        self._item_url_selector = item_url_selector
    
    def parse_response(self, response: scrapy.http.Response) -> typing.List[str]:
        search_content = response.xpath(self._search_content_xpath).get()
        search_result_list = json\
            .loads(search_content)\
            ["content_elements"]
        
        return [
            urllib.parse.urljoin(
                response.url,
                each_result["canonical_url"],
            )
            for each_result
            in search_result_list
        ]
