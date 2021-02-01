# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot.spiders.helpers.sltrib_search_parser as sltrib_search_parser
import newsbot.spiders.helpers.css_link_list_parser as css_link_list_parser
import newsbot.spiders.helpers.xpath_link_list_parser as xpath_link_list_parser
import newsbot.items.news_source as news_source

class NewsSourcesDefinitions(object):
    @classmethod
    def list_all_sources(klass):
        return {
            "Moab @ UPR": news_source.NewsSource(
                name =          "Utah Public Radio",
                url =           "https://www.upr.org/term/moab",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//main//*[@property='dc:title']/a/@href",
                ),
            ),
            "Grand County @ UPR": news_source.NewsSource(
                name =          "Utah Public Radio",
                url =           "https://www.upr.org/term/grand-county",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//main//*[@property='dc:title']/a/@href",
                ),
            ),
            "Moab @ KUER": news_source.NewsSource(
                name =          "KUER 90.1",
                url =           "https://www.kuer.org/term/moab",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//*[@class='term-listing-heading']//*[@property='dc:title']/a/@href",
                ),
            ),
            "Grand County @ KUER": news_source.NewsSource(
                name =          "KUER 90.1",
                url =           "https://www.kuer.org/tags/grand-county",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//*[@class='term-listing-heading']//*[@property='dc:title']/a/@href",
                ),
            ),
            "Kate Groetzinger @ KUER": news_source.NewsSource(
                name =          "KUER 90.1",
                url =           "https://www.kuer.org/people/kate-groetzinger",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    ".AuthorPage-main ps-list-loadmore.ListE ps-promo[data-content-type=news-story] .PromoA-title > a.Link::attr(href)",
                ),
            ),
            "Moab @ SLTrib": news_source.NewsSource(
                name =          "The Salt Lake Tribune",
                url =           "https://www.sltrib.com/search/headlines.basic:Moab",
                links_parser =  sltrib_search_parser.SLTribSearchParser(),
            ),
            "Grand County @ SLTrib": news_source.NewsSource(
                name =          "The Salt Lake Tribune",
                url =           "https://www.sltrib.com/search/headlines.basic:%22Grand%20County%22",
                links_parser =  sltrib_search_parser.SLTribSearchParser(),
            ),
            "Zak Podmore @ SLTrib": news_source.NewsSource(
                name =          "The Salt Lake Tribune",
                url =           "https://www.sltrib.com/author/zpodmore/",
                links_parser =   css_link_list_parser.CSSLinkListParser(
                    ".author-section-page .story > a::attr(href)"
                ),
            ),
            "Moab @ NYT": news_source.NewsSource(
                name =          "The New York Times",
                url =           "https://www.nytimes.com/search?dropmab=false&query=%22Moab%22%2C%20Utah&sort=newest",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//a[contains(@href, 'searchResultPosition')]/@href",
                ),
            ),
            "Moab @ KSL": news_source.NewsSource(
                name =          "KSL",
                url =           "https://www.ksl.com/?sid=53574&nid=208&cx=partner-pub-3771868546990559%3Ar955z1-wmf4&cof=FORID%3A9&ie=ISO-8859-1&sa=Search&searchtype=kslcom&x=15&y=19&q=%22Moab%22#gsc.tab=0&gsc.q=%22Moab%22&gsc.sort=date&gsc.ref=more%3Aksl_news",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//*[@data-refinementlabel='ksl_news']/ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' gs-webResult ')]//a[@class='gs-title']/@href",
                ),
            ),
            "Moab @ WaPo": news_source.NewsSource(
                name =          "The Washington Post",
                url =           "https://www.washingtonpost.com/newssearch/?query=Moab,%20Utah&sort=Date&datefilter=All%20Since%202005&contenttype=Article&contenttype=Video&contenttype=Photo%20Gallery&contenttype=Discussion&contenttype=Live_discussion",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//*[@class='pb-results-container']//a[@data-ng-bind-html='doc.headline']/@href",
                )
            ),
            "Moab @ KUTV": news_source.NewsSource(
                name =          "KUTV",
                url =           "https://kutv.com/search?find=Moab",
                links_parser =  xpath_link_list_parser.XPathLinkListParser(
                    "//*[contains(concat(' ', normalize-space(@class), ' '), ' sd-main-content ')]//li[contains(concat(' ', normalize-space(@class), ' '), ' teaser-list-item ')]/a/@href",
                )
            ),
            "Molly Marcello @ KZMU": news_source.NewsSource(
                name =          "KZMU",
                url =           "https://www.kzmu.org/author/molly-marcello/",
                links_parser =  css_link_list_parser.CSSLinkListParser(
                    ".author-molly-marcello #ajax-content-wrap .main-content article.post .content-inner > .article-content-wrap > .post-header > .title > a::attr(href)",
                ),
            ),
        }
