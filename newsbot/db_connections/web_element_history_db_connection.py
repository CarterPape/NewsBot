# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import difflib
import logging
import scrapy.settings
from newsbot.db_connections import db_connection
from newsbot.items import emailable_item
from newsbot.items import web_element


class WebElementHistoryDBConnection(db_connection.DBConnection):
    pass
