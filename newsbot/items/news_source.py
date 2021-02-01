# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import newsbot.spiders.helpers.link_list_parser as link_list_parser


class NewsSource(object):
    def __init__(self, *,
        source_id: str,
        name: str,
        url: str,
        links_parser: link_list_parser.LinkListParser,
    ):
        self.source_id =    source_id
        self.name =         name
        self.url =          url
        self.links_parser = links_parser
