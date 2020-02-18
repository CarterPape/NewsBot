# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import NewsBot.db_connection_loader
import scrapy.utils.project

DB_NAME = "newsbot"
project_settings = scrapy.utils.project.get_project_settings()
