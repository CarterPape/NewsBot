# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import newsbot.spiders.helpers.sltrib_search_parser as sltrib_search_parser
import newsbot.spiders.helpers.css_link_list_parser as css_link_list_parser
import newsbot.spiders.helpers.xpath_link_list_parser as xpath_link_list_parser
import newsbot.spiders.helpers.json_link_list_parser as json_link_list_parser
import newsbot.items.news_source as news_source

class NewsSourcesDefinitions(object):
    _all_sources = [
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "Utah Public Radio",
            home_url =      "https://www.upr.org",
            search_url_list = [
                "https://www.upr.org/term/moab",
                "https://www.upr.org/term/grand-county",
            ],
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
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
            links_parser =  css_link_list_parser.CSSLinkListParser(
                "ps-list-loadmore.ListE ps-promo[data-content-type=news-story] .PromoA-title > a.Link::attr(href)",
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
            links_parser =  sltrib_search_parser.SLTribSearchParser(),
        ),
        #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
        news_source.NewsSource(
            source_id =     "Zak Podmore @ SLTrib",
            name =          "The Salt Lake Tribune",
            home_url =      "https://www.sltrib.com",
            search_url_list = [
                "https://www.sltrib.com/author/zpodmore/",
            ],
            links_parser =   css_link_list_parser.CSSLinkListParser(
                ".author-section-page .story > a::attr(href)"
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "The New York Times",
            home_url =      "https://www.nytimes.com",
            search_url_list = [
                "https://www.nytimes.com/search?dropmab=false&query=%22Moab%22%2C%20Utah&sort=newest",
            ],
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//a[contains(@href, 'searchResultPosition')]/@href",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "KSL",
            home_url =      "https://www.ksl.com",
            search_url_list = [
                "https://www.ksl.com/?sid=53574&nid=208&cx=partner-pub-3771868546990559%3Ar955z1-wmf4&cof=FORID%3A9&ie=ISO-8859-1&sa=Search&searchtype=kslcom&x=15&y=19&q=%22Moab%22#gsc.tab=0&gsc.q=%22Moab%22&gsc.sort=date&gsc.ref=more%3Aksl_news",
            ],
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//*[@data-refinementlabel='ksl_news']/ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' gs-webResult ')]//a[@class='gs-title']/@href",
            ),
        ),
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        news_source.NewsSource(
            name =          "The Washington Post",
            home_url =      "https://www.washingtonpost.com",
            search_url_list = [
                "https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5B*+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:(%22Article%22+OR+%22Video%22+OR+%22Photo+Gallery%22+OR+%22Discussion%22+OR+%22Live_discussion%22)&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query=Moab,+Utah&sort=displaydatetime+desc",
            ],
            request_headers =   {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 "
                    "Safari/605.1.15"
                ),
            },
            links_parser =  json_link_list_parser.JSONLinkListParser(
                item_list_selector = (
                    lambda base_object: base_object["results"]["documents"]
                ),
                item_url_selector = (
                    lambda result_object: result_object["contenturl"]
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
                    lambda base_object: base_object["content"]["component-search-result_list-v1-01"]["search"]["teasers"]
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
            links_parser =  css_link_list_parser.CSSLinkListParser(
                ".author-molly-marcello #ajax-content-wrap .main-content article.post .content-inner > .article-content-wrap > .post-header > .title > a::attr(href)",
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
            links_parser =  css_link_list_parser.CSSLinkListParser(
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
    def list_all_sources(klass) -> typing.List[news_source.NewsSource]:
        return klass._all_sources
