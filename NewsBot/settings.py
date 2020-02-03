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

import environment
import scrapy.utils.conf
import os
import os.path
import keyring
import NewsBot.log_formatter

BOT_NAME    = "NewsBot"
_BOT_VERSION = "0.0.2"

SPIDER_MODULES      = ["NewsBot.spiders"]
NEWSPIDER_MODULE    = "NewsBot.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = f"{BOT_NAME}/{_BOT_VERSION} (+https://github.com/carterpape/newsbot)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#   "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "NewsBot.middlewares.NewsbotSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "NewsBot.middlewares.NewsbotDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    
}

_PROJECT_ROOT_DIRECTORY = \
    os.path.dirname(
        scrapy.utils.conf.closest_scrapy_cfg()
    )

_DATA_DIRECTORY = \
    os.path.abspath(
        os.path.join(
            _PROJECT_ROOT_DIRECTORY,
            "data/",
        )
    )
os.makedirs(_DATA_DIRECTORY, exist_ok = True)

_LOG_DIRECTORY = \
    os.path.abspath(
        os.path.join(
            _PROJECT_ROOT_DIRECTORY,
            "log/",
        )
    )
os.makedirs(_LOG_DIRECTORY, exist_ok = True)

LOG_FILE = \
    os.path.abspath(
        os.path.join(
            _LOG_DIRECTORY,
            f"{BOT_NAME}-{_BOT_VERSION}.log",
        )
    )
LOG_LEVEL = "WARNING"
LOG_FORMATTER = "NewsBot.log_formatter.NewsBotLogFormatter"

# MAIL_FROM   = environment.EMAIL_SENDER
# MAIL_HOST   = environment.SMTP_HOST
# MAIL_PORT   = environment.SMTP_PORT
# MAIL_USER   = environment.EMAIL_SENDER
# MAIL_PASS   = keyring.get_password(
#     service_name    = environment.EMAIL_SERVICE_NAME,
#     username        = MAIL_USER,
# )
# MAIL_TLS    = environment.USE_STARTTLS_WITH_MAIL
# MAIL_SSL    = environment.USE_SSL_WITH_MAIL

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

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
