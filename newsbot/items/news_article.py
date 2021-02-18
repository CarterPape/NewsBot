# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import newsbot.items.emailable_item as emailable_item
import string
import pape.utilities
import urllib.parse


class NewsArticle(emailable_item.EmailableItem):
    clean_url =     scrapy.Field()
    title =         scrapy.Field(ignore_when_serializing = True)
    description =   scrapy.Field(ignore_when_serializing = True)
    img_src =       scrapy.Field(ignore_when_serializing = True)
    news_source =   scrapy.Field(ignore_when_serializing = True)
    
    def synthesize_email_subject(self) -> str:
        return f"{self['news_source'].name}: {self['title']}"
    
    def synthesize_html_email_body(self) -> str:
        return self._get_email_template().safe_substitute({
            "email_subject":            self.synthesize_email_subject(),
            "news_source_name":         self["news_source"].name,
            "news_source_home_url":     self["news_source"].home_url,
            "news_source_search_url":   self["news_source"].search_url,
            "article_title":            self["title"],
            "article_description":      self["description"],
            "article_url":              self["clean_url"],
            "article_domain":           urllib.parse.urlparse(self["clean_url"]).netloc,
        })
