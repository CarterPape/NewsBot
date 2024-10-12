# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import dataclasses

from newsbot.spiders.helpers import css_link_list_parser
from newsbot.spiders.helpers import xpath_link_list_parser
from newsbot.spiders.helpers import json_link_list_parser
from newsbot.items import news_source
from newsbot.items import google_custom_search_news_source

@dataclasses.dataclass
class NewsSourcesDefinitions:
    _all_sources = [
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "Utah Public Radio",
            home_url =      "https://www.upr.org",
            search_url_list = [
                "https://www.upr.org/term/moab",
                "https://www.upr.org/term/grand-county",
            ],
            links_parser = xpath_link_list_parser.XPathLinkListParser(
                "//main//*[@property='dc:title']/a/@href",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "KUER 90.1",
            home_url =      "https://www.kuer.org",
            search_url_list = [
                "https://www.kuer.org/tags/moab",
                "https://www.kuer.org/tags/grand-county",
                "https://www.kuer.org/people/kate-groetzinger",
            ],
            links_parser = css_link_list_parser.CSSLinkListParser(
                "ps-list-loadmore.ListE "
                "ps-promo[data-content-type=news-story] "
                ".PromoA-title > a.Link::attr(href)",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "The Salt Lake Tribune",
            home_url =      "https://www.sltrib.com",
            search_url_list = [
                "https://www.sltrib.com/search/headlines.basic:Moab",
                "https://www.sltrib.com/search/headlines.basic:%22Grand%20County%22",
            ],
            links_parser =  json_link_list_parser.JSONLinkListParser(
                json_extractor = (
                    lambda response: response.xpath("//*[@title='Search Results']/@content").get()
                ),
                item_list_selector = (
                    lambda base_object: base_object["content_elements"]
                ),
                item_url_selector = (
                    lambda each_result: each_result["canonical_url"]
                )
            ),
        ),
        #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
        news_source.NewsSource(
            source_id =     "Zak Podmore @ SLTrib",
            name =          "The Salt Lake Tribune",
            home_url =      "https://www.sltrib.com",
            search_url_list = [
                "https://www.sltrib.com/author/zpodmore/",
            ],
            links_parser = css_link_list_parser.CSSLinkListParser(
                ".author-section-page .story > a::attr(href)"
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "The New York Times",
            home_url =      "https://www.nytimes.com",
            search_url_list = [
                "https://www.nytimes.com/search"
                "?dropmab=false&query=%22Moab%22%2C%20Utah&sort=newest",
            ],
            links_parser = xpath_link_list_parser.XPathLinkListParser(
                "//a[contains(@href, 'searchResultPosition')]/@href",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "The Washington Post",
            home_url =      "https://www.washingtonpost.com",
            search_url_list = [
                "https://www.washingtonpost.com/search/api/search/",
            ],
            request_method = "POST",
            request_headers = {
                "User-Agent": "WaPoAPI_UA/site-search",
                "Referer": "https://www.washingtonpost.com/search/?query=Moab%2C+Utah",
            },
            links_parser = json_link_list_parser.JSONLinkListParser(
                item_list_selector = (
                    lambda base_object: base_object["body"]["items"]
                ),
                item_url_selector = (
                    lambda each_result: each_result["link"]
                ),
            )
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "KUTV",
            home_url =      "https://kutv.com",
            search_url_list = [
                "https://kutv.com/search?find=Moab",
            ],
            links_parser =  json_link_list_parser.JSONLinkListParser(
                json_extractor = (
                    lambda response: response.css(
                        "script[data-prerender='facade'][type='application/json']::text"
                    ).get()
                ),
                item_list_selector = (
                    lambda base_object: base_object\
                        ["content"]\
                        ["component-search-result_list-v1-01"]\
                        ["search"]\
                        ["teasers"]
                ),
                item_url_selector = (
                    lambda result_object: result_object["url"]
                ),
            )
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "KZMU",
            home_url =      "https://kzmu.org",
            search_url_list = [
                "https://www.kzmu.org/author/molly-marcello/",
            ],
            links_parser = css_link_list_parser.CSSLinkListParser(
                ".author-molly-marcello "
                "#ajax-content-wrap "
                ".main-content "
                "article.post "
                ".content-inner"
                "> .article-content-wrap"
                "> .post-header"
                "> .title"
                "> a::attr(href)",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "ABC4",
            home_url =      "https://www.abc4.com",
            search_url_list = [
                "https://www.abc4.com/?s=Moab&submit=Search&orderby=modified",
                "https://www.abc4.com/?s=%22Grand+County%22&submit=Search&orderby=modified"
            ],
            links_parser = css_link_list_parser.CSSLinkListParser(
                "main article a::attr(href)"
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "FOX13",
            home_url =      "https://www.fox13now.com",
            search_url_list =[
                "https://www.fox13now.com/search?q=Moab&s=1",
            ],
            links_parser = css_link_list_parser.CSSLinkListParser(
                ".Page-results a::attr(href)"
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        google_custom_search_news_source.GoogleCustomSearchNewsSource(
            name =          "Deseret News",
            home_url =      "https://www.deseret.com",
            cx =            "4a9479158a6d21f33",
        ),
        google_custom_search_news_source.GoogleCustomSearchNewsSource(
            name =          "KSL",
            home_url =      "https://www.ksl.com",
            cx =            "partner-pub-3771868546990559:r955z1-wmf4",
        ),
        google_custom_search_news_source.GoogleCustomSearchNewsSource(
            name =          "Moab Custom News Search",
            home_url =      "https://cse.google.com/cse?cx=8f6af2addb691b859",
            cx =            "8f6af2addb691b859",
        ),
    ]
    
    @classmethod
    def list_all_sources(klass) -> list[news_source.NewsSource]:
        return klass._all_sources
