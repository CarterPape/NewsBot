# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import os
import locale
import logging
import twisted.internet.reactor
import scrapy.utils.log
import scrapy.utils.project
import scrapy.spiderloader
import dotenv

from newsbot.tasking import job_registry
from newsbot import db_builder

dotenv.load_dotenv(dotenv.find_dotenv())
locale.setlocale(locale.LC_ALL, '')

os.environ["SCRAPY_SETTINGS_MODULE"] = "newsbot.settings"
project_settings = scrapy.utils.project.get_project_settings()

scrapy.utils.log.configure_logging(settings = project_settings)
stderr_stream_handler = logging.StreamHandler()
stderr_stream_handler.setLevel("WARNING")
logging.getLogger().addHandler(stderr_stream_handler)

db_builder = db_builder.DBBuilder(from_settings = project_settings)
db_builder.build_unbuilt_tables()

spider_loader = scrapy.spiderloader.SpiderLoader(project_settings)
spider_classes = [
    spider_loader.load(spider_name)
    for spider_name
    in spider_loader.list()
]

registry = job_registry.NewsBotJobRegistry(
    from_spider_classes = spider_classes,
)

registry.schedule_all_jobs()
twisted.internet.reactor.run() # type: ignore # pylint: disable=no-member
