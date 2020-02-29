# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing_extensions


class CrawlScheduler(typing_extensions.Protocol):
    @property
    def pause_time_in_seconds(self) -> float:
        raise NotImplementedError
