# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.crawler
import scrapy.utils.project
import NewsBot.spiders

process = scrapy.crawler.CrawlerProcess(scrapy.utils.project.get_project_settings())
process.crawl(NewsBot.spiders.DispatchCallLogSpider)
process.start() # the script will block here until all crawling jobs are finished
