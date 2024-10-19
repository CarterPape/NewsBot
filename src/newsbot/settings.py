# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

# Scrapy settings for NewsBot project
#
# You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import os.path
import datetime

import scrapy.utils.conf
import dotenv

from newsbot.items import item_with_files
from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler

dotenv.load_dotenv(dotenv.find_dotenv())

_ENVIRONMENT = os.getenv("ENVIRONMENT")

_PROJECT_DIRECTORY = (
    os.path.abspath(
        os.path.dirname(
            scrapy.utils.conf.closest_scrapy_cfg(
                path = os.path.realpath(__file__)
            )
        )
    )
)


BOT_NAME = "NewsBot"

with open(os.path.abspath(
    os.path.join(
        _PROJECT_DIRECTORY,
        "VERSION",
    )
), "r", encoding="utf-8") as version_file:
    _BOT_VERSION = version_file.read().strip()

_TOP_LEVEL_MODULES = ["newsbot"]

SPIDER_MODULES = [
    top_level_module + ".spiders"
    for top_level_module in _TOP_LEVEL_MODULES
]
NEWSPIDER_MODULE = SPIDER_MODULES[0]

_DB_CONNECTION_MODULES = [
    top_level_module + ".db_connections"
    for top_level_module in _TOP_LEVEL_MODULES
]


if _ENVIRONMENT == "development":
    USER_AGENT = (
        f"{BOT_NAME}-under-development/{_BOT_VERSION} (+https://github.com/carterpape/newsbot)"
    )
else:
    USER_AGENT = f"{BOT_NAME}/{_BOT_VERSION} (+https://github.com/carterpape/newsbot)"

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True


_DATA_DIRECTORY = (
    os.path.abspath(
        os.path.join(
            _PROJECT_DIRECTORY,
            "data/",
        )
    )
)

FILES_STORE = (
    os.path.abspath(
        os.path.join(
            _DATA_DIRECTORY,
            "downloads/",
        )
    )
)

FILES_URLS_FIELD = item_with_files.ItemWithFiles.get_files_urls_field()
FILES_RESULT_FIELD = item_with_files.ItemWithFiles.get_files_result_field()

DOWNLOAD_WARNSIZE = 9 * (10 ** 6)


if _ENVIRONMENT == "development":
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = "WARNING"

_LOG_DIRECTORY = (
    os.path.abspath(
        os.path.join(
            _PROJECT_DIRECTORY,
            "log/",
        )
    )
)

LOG_FILE = (
    os.path.abspath(
        os.path.join(
            _LOG_DIRECTORY,
            f"{BOT_NAME}-{_BOT_VERSION}.log",
        )
    )
)

LOG_FORMATTER = "newsbot.log_formatter.NewsBotLogFormatter"

TELNETCONSOLE_ENABLED = True


_EMAIL_SENDER =         os.getenv("DEFAULT_EMAIL_SENDER")
_EMAIL_SENDER_DOMAIN =  os.getenv("EMAIL_SENDER_DOMAIN")

_MAILGUN_API_KEY =      os.getenv("MAILGUN_API_KEY")

_MYSQL_DATABASE =       os.getenv("MYSQL_DATABASE")
_MYSQL_USER =           os.getenv("MYSQL_USER")
_MYSQL_PASSWORD =       os.getenv("MYSQL_PASSWORD")

_PRINT_INSTEAD_OF_EMAIL = (_ENVIRONMENT == "development")


# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
AUTOTHROTTLE_DEBUG = True

DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1


if _ENVIRONMENT == "development":
    _FORCE_SCHEDULER = (
        uniformly_random_scheduler.UniformlyRandomScheduler(
            minimum_interval = datetime.timedelta(seconds = 60),
            maximum_interval = datetime.timedelta(seconds = 80),
            first_call_is_immediate =   True,
        )
    )
