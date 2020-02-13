# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot_tasking.job_registry
import NewsBot.spiders.self_scheduling_spider
import twisted.internet.reactor
import scrapy.utils.log
import scrapy.utils.project
import os
import scrapy.spiderloader

os.environ["SCRAPY_SETTINGS_MODULE"] = "NewsBot.settings"
project_settings = scrapy.utils.project.get_project_settings()
scrapy.utils.log.configure_logging(settings = project_settings)

spider_loader = scrapy.spiderloader.SpiderLoader(project_settings)
spider_classes = [
    spider_loader.load(spider_name)
    for spider_name in spider_loader.list()
]

registry = newsbot_tasking.job_registry.NewsBotJobRegistry(
    from_spider_classes = spider_classes,
)

registry.schedule_all_jobs()
twisted.internet.reactor.run()
