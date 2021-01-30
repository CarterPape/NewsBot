# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import scrapy.logformatter
import newsbot.exceptions.safe_drop_exception as safe_drop_exception


class NewsBotLogFormatter(scrapy.logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        if isinstance(exception, safe_drop_exception.SafeDropException):
            return {
                "level":    logging.DEBUG,
                "msg":      scrapy.logformatter.DROPPEDMSG,
                "args": {
                    "exception":    exception,
                    "item":         item,
                },
            }
        else:
            return super().dropped(
                item,
                exception,
                response,
                spider,
            )
