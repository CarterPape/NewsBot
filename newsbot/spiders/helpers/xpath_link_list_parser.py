# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot.spiders.helpers.lambda_link_list_parser as lambda_link_list_parser

class XPathLinkListParser(lambda_link_list_parser.LambdaLinkListParser):
    def __init__(self, link_xpath: str):
        self._link_lambda = (
            lambda response: response.xpath(link_xpath).getall()
        )
