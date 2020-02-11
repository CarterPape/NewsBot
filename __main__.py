# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot_tasking
import NewsBot.spiders
import twisted.internet.reactor
import scrapy.utils.log
import scrapy.utils.project

scrapy.utils.log.configure_logging(settings = scrapy.utils.project.get_project_settings())

registry = newsbot_tasking.NewsBotJobRegistry(
    from_spider_classes = NewsBot.spiders.SelfScheduling.__subclasses__(),
)

registry.schedule_all_jobs()
twisted.internet.reactor.run()
