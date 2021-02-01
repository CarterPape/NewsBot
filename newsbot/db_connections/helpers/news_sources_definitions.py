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
import newsbot.items.news_source as news_source

class NewsSourcesDefinitions(object):
    _all_sources = [
        news_source.NewsSource(
            source_id =     "Moab @ UPR",
            name =          "Utah Public Radio",
            url =           "https://www.upr.org/term/moab",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//main//*[@property='dc:title']/a/@href",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Grand County @ UPR",
            name =          "Utah Public Radio",
            url =           "https://www.upr.org/term/grand-county",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//main//*[@property='dc:title']/a/@href",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Moab @ KUER",
            name =          "KUER 90.1",
            url =           "https://www.kuer.org/term/moab",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//*[@class='term-listing-heading']//*[@property='dc:title']/a/@href",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Grand County @ KUER",
            name =          "KUER 90.1",
            url =           "https://www.kuer.org/tags/grand-county",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//*[@class='term-listing-heading']//*[@property='dc:title']/a/@href",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Kate Groetzinger @ KUER",
            name =          "KUER 90.1",
            url =           "https://www.kuer.org/people/kate-groetzinger",
            links_parser =  css_link_list_parser.CSSLinkListParser(
                ".AuthorPage-main ps-list-loadmore.ListE ps-promo[data-content-type=news-story] .PromoA-title > a.Link::attr(href)",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Moab @ SLTrib",
            name =          "The Salt Lake Tribune",
            url =           "https://www.sltrib.com/search/headlines.basic:Moab",
            links_parser =  sltrib_search_parser.SLTribSearchParser(),
        ),
        news_source.NewsSource(
            source_id =     "Grand County @ SLTrib",
            name =          "The Salt Lake Tribune",
            url =           "https://www.sltrib.com/search/headlines.basic:%22Grand%20County%22",
            links_parser =  sltrib_search_parser.SLTribSearchParser(),
        ),
        news_source.NewsSource(
            source_id =     "Zak Podmore @ SLTrib",
            name =          "The Salt Lake Tribune",
            url =           "https://www.sltrib.com/author/zpodmore/",
            links_parser =   css_link_list_parser.CSSLinkListParser(
                ".author-section-page .story > a::attr(href)"
            ),
        ),
        news_source.NewsSource(
            source_id =     "Moab @ NYT",
            name =          "The New York Times",
            url =           "https://www.nytimes.com/search?dropmab=false&query=%22Moab%22%2C%20Utah&sort=newest",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//a[contains(@href, 'searchResultPosition')]/@href",
            ),
        ),
        news_source.NewsSource(
            source_id =     "Moab @ KSL",
            name =          "KSL",
            url =           "https://www.ksl.com/?sid=53574&nid=208&cx=partner-pub-3771868546990559%3Ar955z1-wmf4&cof=FORID%3A9&ie=ISO-8859-1&sa=Search&searchtype=kslcom&x=15&y=19&q=%22Moab%22#gsc.tab=0&gsc.q=%22Moab%22&gsc.sort=date&gsc.ref=more%3Aksl_news",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//*[@data-refinementlabel='ksl_news']/ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' gs-webResult ')]//a[@class='gs-title']/@href",
            ),
        ),
        # news_source.NewsSource(
        #     source_id =     "Moab @ WaPo",
        #     name =          "The Washington Post",
        #     url =           "https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5B*+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:(%22Article%22+OR+%22Video%22+OR+%22Photo+Gallery%22+OR+%22Discussion%22+OR+%22Live_discussion%22)&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query=Moab,+Utah&sort=displaydatetime+desc&callback=angular.callbacks._0",
        #     links_parser =  xpath_link_list_parser.XPathLinkListParser(
        #         "//*[@class='pb-results-container']//a[@data-ng-bind-html='doc.headline']/@href",
        #     )
        # ),
        news_source.NewsSource(
            source_id =     "Moab @ KUTV",
            name =          "KUTV",
            url =           "https://kutv.com/search?find=Moab",
            links_parser =  xpath_link_list_parser.XPathLinkListParser(
                "//*[contains(concat(' ', normalize-space(@class), ' '), ' sd-main-content ')]//li[contains(concat(' ', normalize-space(@class), ' '), ' teaser-list-item ')]/a/@href",
            )
        ),
        news_source.NewsSource(
            source_id =     "Molly Marcello @ KZMU",
            name =          "KZMU",
            url =           "https://www.kzmu.org/author/molly-marcello/",
            links_parser =  css_link_list_parser.CSSLinkListParser(
                ".author-molly-marcello #ajax-content-wrap .main-content article.post .content-inner > .article-content-wrap > .post-header > .title > a::attr(href)",
            ),
        ),
    ]
    
    @classmethod
    def list_all_sources(klass) -> typing.List[news_source.NewsSource]:
        return klass._all_sources
