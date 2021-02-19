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
import newsbot.spiders.helpers.lambda_link_list_parser as lambda_link_list_parser

class CSSLinkListParser(lambda_link_list_parser.LambdaLinkListParser):
    def __init__(self, link_css: str):
        self._link_lambda = (
            lambda response: response.css(link_css).getall()
        )
