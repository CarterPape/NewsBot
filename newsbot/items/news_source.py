# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing

from newsbot.spiders.helpers import link_list_parser


class NewsSource:
    def __init__(self, *,
        source_id: str = None,
        name: str,
        home_url: str,
        search_url_list: typing.List[str],
        request_headers: dict = None,
        links_parser: link_list_parser.LinkListParser,
    ):
        if source_id is not None:
            self.source_id = source_id
        else:
            self.source_id = name
        
        self.name =             name
        self.home_url =         home_url
        self.search_url_list =  search_url_list
        self.request_headers =  request_headers
        self.links_parser =     links_parser
        
    def __str__(self):
        return f"{self.name} (search urls: {self.search_url_list})"
