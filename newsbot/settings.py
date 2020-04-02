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

import dotenv
import scrapy.utils.conf
import os
import os.path
import datetime
import newsbot.items.item_with_files as item_with_files

dotenv.load_dotenv(dotenv.find_dotenv())

BOT_NAME =      "NewsBot"
_BOT_VERSION =  "0.2.0"

_TOP_LEVEL_MODULES   = ["private", "newsbot"]

SPIDER_MODULES =    [
    top_level_module + ".spiders"
    for top_level_module in _TOP_LEVEL_MODULES
]
NEWSPIDER_MODULE =  SPIDER_MODULES[0]

_DB_CONNECTION_MODULES =    [
    top_level_module + ".db_connections"
    for top_level_module in _TOP_LEVEL_MODULES
]


_ENVIRONMENT =          os.getenv("ENVIRONMENT")


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = f"{BOT_NAME}/{_BOT_VERSION} (+https://github.com/carterpape/newsbot)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

_PROJECT_DIRECTORY = (
    os.path.abspath(
        os.path.dirname(
            scrapy.utils.conf.closest_scrapy_cfg(
                path = os.path.realpath(__file__)
            )
        )
    )
)

_DATA_DIRECTORY = (
    os.path.abspath(
        os.path.join(
            _PROJECT_DIRECTORY,
            "data/",
        )
    )
)
os.makedirs(_DATA_DIRECTORY, exist_ok = True)

FILES_STORE = (
    os.path.abspath(
        os.path.join(
            _DATA_DIRECTORY,
            "downloads/",
        )
    )
)
os.makedirs(FILES_STORE, exist_ok = True)

FILES_URLS_FIELD = item_with_files.ItemWithFiles.get_files_urls_field()
FILES_RESULT_FIELD = item_with_files.ItemWithFiles.get_files_result_field()


if _ENVIRONMENT == "development":
    LOG_LEVEL = "INFO"
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
os.makedirs(_LOG_DIRECTORY, exist_ok = True)

LOG_FILE = (
    os.path.abspath(
        os.path.join(
            _LOG_DIRECTORY,
            f"{BOT_NAME}-{_BOT_VERSION}.log",
        )
    )
)

LOG_FORMATTER = "newsbot.log_formatter.NewsBotLogFormatter"

_EMAIL_SENDER =         os.getenv("DEFAULT_EMAIL_SENDER")
_EMAIL_SENDER_DOMAIN =  os.getenv("EMAIL_SENDER_DOMAIN")

_MAILGUN_API_KEY =      os.getenv("MAILGUN_API_KEY")

_MYSQL_DATABASE =       os.getenv("MYSQL_DATABASE")
_MYSQL_USER =           os.getenv("MYSQL_USER")
_MYSQL_PASSWORD =       os.getenv("MYSQL_PASSWORD")

_PRINT_INSTEAD_OF_EMAIL = (os.getenv("ENVIRONMENT") == "development")

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
