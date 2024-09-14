# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=too-many-arguments

import typing
import dataclasses

from newsbot.spiders.helpers import link_list_parser

@dataclasses.dataclass
class NewsSource:
    def __init__(self, *,
        source_id: str | None = None,
        name: str,
        home_url: str,
        search_url_list: typing.Iterable[str],
        request_method: str = "GET",
        request_headers: dict | None = None,
        links_parser: link_list_parser.LinkListParser,
    ):
        if source_id is not None:
            self.source_id = source_id
        else:
            self.source_id = name
        
        self.name =             name
        self.home_url =         home_url
        self.search_url_list =  search_url_list
        self.request_method =   request_method
        self.request_headers =  request_headers
        self.links_parser =     links_parser
        
    def __str__(self):
        return f"{self.name} (search urls: {self.search_url_list})"
