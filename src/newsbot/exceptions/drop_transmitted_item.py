# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

from newsbot.exceptions import safe_drop_exception

class DropTransmittedItem(safe_drop_exception.SafeDropException):
    pass
