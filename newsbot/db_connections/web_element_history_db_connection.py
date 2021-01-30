# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import difflib
import logging
import scrapy.settings
import newsbot.db_connections.db_connection as db_connection
import newsbot.items.emailable_item as emailable_item
import newsbot.items.web_element as web_element


class WebElementHistoryDBConnection(db_connection.DBConnection):
    pass
