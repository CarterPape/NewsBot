# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import abc


class Logger(
    object,
    metaclass = abc.ABCMeta,
):
    @property
    def _logger(self):
        if getattr(self, "__logger", None) != None:
            pass
        else:
            self.__logger = logging.getLogger(type(self).__name__)
        
        return self.__logger
