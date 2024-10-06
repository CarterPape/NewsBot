# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections.abc
import os
import dataclasses

import dotenv

from newsbot.items import news_source
from newsbot.spiders.helpers import json_link_list_parser


dotenv.load_dotenv(dotenv.find_dotenv())

@dataclasses.dataclass
class GoogleCustomSearchNewsSource(news_source.NewsSource):
    def __init__(self, *,
        name: str,
        home_url: str,
        cx: str,
    ):
        search_url_list = self.generate_search_url_list(cx = cx)
        
        super().__init__(
            source_id =         name,
            name =              name,
            home_url =          home_url,
            search_url_list =   search_url_list,
            links_parser =      json_link_list_parser.JSONLinkListParser(
                item_list_selector = (
                    lambda base_object: base_object["items"]
                ),
                item_url_selector = (
                    lambda result_object: result_object["link"]
                )
            )
        )
    
    def generate_search_url_list(self, *,
        cx: str,
    ) -> collections.abc.Iterable[str]:
        key = os.getenv("GOOGLE_CSE_API_KEY")
        
        yield (
            "https://customsearch.googleapis.com/customsearch/v1/siterestrict"
            f"?cx={cx}"
            "&exactTerms=Moab"
            "&q=%22Utah%22"
            "&sort=date"
            f"&key={key}"
        )
        yield (
            "https://customsearch.googleapis.com/customsearch/v1/siterestrict"
            f"?cx={cx}"
            "&q=%22Grand%20County%22%20%22Utah%22"
            "&sort=date"
            f"&key={key}"
        )
