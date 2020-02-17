# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging


class Logger(object):
    @property
    def _logger(self):
        if hasattr(self, "_logger") and self._logger != None:
            pass
        else:
            self._logger = logging.getLogger(type(self).__name__)
        
        return self._logger
