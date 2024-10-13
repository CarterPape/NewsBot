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

def main():
    dotenv.load_dotenv(dotenv.find_dotenv())
    locale.setlocale(locale.LC_ALL, '')
    
    os.environ["SCRAPY_SETTINGS_MODULE"] = "newsbot.settings"
    project_settings = scrapy.utils.project.get_project_settings()
    
    data_directory = project_settings.get("_DATA_DIRECTORY")
    logging.debug(f"Making data directory {data_directory}")
    os.makedirs(data_directory, exist_ok = True)
    
    files_store = project_settings.get("FILES_STORE")
    logging.debug(f"Making files store {files_store}")
    os.makedirs(files_store, exist_ok = True)
    
    log_directory = project_settings.get("_LOG_DIRECTORY")
    logging.debug(f"Making log directory {log_directory}")
    os.makedirs(log_directory, exist_ok = True)
    
    scrapy.utils.log.configure_logging(settings = project_settings)
    stderr_stream_handler = logging.StreamHandler()
    stderr_stream_handler.setLevel(project_settings.get("LOG_LEVEL"))
    logging.getLogger().addHandler(stderr_stream_handler)
    
    logging.debug(
        "Logging configured with log level "
        f"{logging.getLevelName(stderr_stream_handler.level)} "
        f"({stderr_stream_handler.level})"
    )
    
    logging.debug("Settings loaded:")
    for key, value in project_settings.items():
        logging.debug(f"{key} = {value}")
    
    the_db_builder = db_builder.DBBuilder(from_settings = project_settings)
    the_db_builder.build_unbuilt_tables()
    
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

if __name__ == "__main__":
    main()
