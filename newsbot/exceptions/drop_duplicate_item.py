# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import newsbot.exceptions.safe_drop_exception as safe_drop_exception

class DropDuplicateItem(safe_drop_exception.SafeDropException):
    pass
