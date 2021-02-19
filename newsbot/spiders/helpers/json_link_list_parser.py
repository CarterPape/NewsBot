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
        json_string =   self._json_extractor(response)
        json_object =   json.loads(json_string)
        item_list =     self._item_list_selector(json_object)
        
        return [
            urllib.parse.urljoin(
                response.url,
                self._item_url_selector(each_item),
            )
            for each_item
            in item_list
        ]
