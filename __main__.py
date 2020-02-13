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

os.environ["SCRAPY_SETTINGS_MODULE"] = "NewsBot.settings"
scrapy.utils.log.configure_logging(settings = scrapy.utils.project.get_project_settings())

registry = newsbot_tasking.job_registry.NewsBotJobRegistry(
    from_spider_classes = NewsBot.spiders.self_scheduling_spider.SelfScheduling.__subclasses__(),
)

registry.schedule_all_jobs()
twisted.internet.reactor.run()
