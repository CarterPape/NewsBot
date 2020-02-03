# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import scrapy.logformatter

class NewsBotLogFormatter(scrapy.logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            "level":    logging.INFO,
            "msg":      scrapy.logformatter.DROPPEDMSG,
            "args": {
                "exception":    exception,
                "item":         item,
            },
        }
