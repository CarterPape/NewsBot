# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import abc
import typing
import urllib.parse
import scrapy.http

class LinkListParser(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def parse_response(self, response: scrapy.http.Response) -> typing.List[str]:
        pass
    
    def _join_urls_with_common_base(self, *,
        common_base: str,
        urls: typing.List[str]
    ):
        return [
            urllib.parse.urljoin(
                common_base,
                each_url,
            )
            for each_url
            in urls
        ]
