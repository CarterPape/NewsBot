# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import twisted.internet.reactor
import scrapy.utils.log
import scrapy.utils.project
import os
import scrapy.spiderloader
import dotenv
import logging
import newsbot.tasking.job_registry as job_registry
import newsbot.db_connections.db_connection
import newsbot.concrete_subclass_loader

dotenv.load_dotenv(dotenv.find_dotenv())

os.environ["SCRAPY_SETTINGS_MODULE"] = "newsbot.settings"
project_settings = scrapy.utils.project.get_project_settings()

scrapy.utils.log.configure_logging(settings = project_settings)
sterr_stream_handler = logging.StreamHandler()
sterr_stream_handler.setLevel("WARNING")
logging.getLogger().addHandler(sterr_stream_handler)

db_connection_loader = newsbot.concrete_subclass_loader.ConcreteSubclassLoader(
    load_subclasses_of =    newsbot.db_connections.db_connection.DBConnection,
    from_modules_named =    project_settings.getlist("_TOP_LEVEL_MODULES"),
)
db_connection_list = [
    db_connection_class(settings = project_settings)
    for db_connection_class in db_connection_loader.list()
]

for db_connection in db_connection_list:
    if db_connection.table_exists():
        pass
    else:
        db_connection.create_table()
    db_connection.close()

spider_loader = scrapy.spiderloader.SpiderLoader(project_settings)
spider_classes = [
    spider_loader.load(spider_name)
    for spider_name in spider_loader.list()
]

registry = job_registry.NewsBotJobRegistry(
    from_spider_classes = spider_classes,
)

registry.schedule_all_jobs()
twisted.internet.reactor.run()
