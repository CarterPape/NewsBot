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
import keyring
import NewsBot.log_formatter
import datetime

dotenv.load_dotenv(dotenv.find_dotenv())

BOT_NAME =      "NewsBot"
_BOT_VERSION =  "0.1.0"

SPIDER_MODULES =    ["NewsBot.spiders"]
NEWSPIDER_MODULE =  "NewsBot.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = f"{BOT_NAME}/{_BOT_VERSION} (+https://github.com/carterpape/newsbot)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

if os.getenv("ENVIRONMENT") == "development":
    LOG_LEVEL = "INFO"
else:
    LOG_LEVEL = "WARNING"

_PROJECT_DIRECTORY = (
    os.path.dirname(
        scrapy.utils.conf.closest_scrapy_cfg(
            path = os.path.realpath(__file__)
        )
    )
)

LOG_FORMATTER = "NewsBot.log_formatter.NewsBotLogFormatter"

_DATA_DIRECTORY = (
    os.path.abspath(
        os.path.join(
            _PROJECT_DIRECTORY,
            "data/",
        )
    )
)
os.makedirs(_DATA_DIRECTORY, exist_ok = True)


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

