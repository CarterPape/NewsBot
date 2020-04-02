# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import abc


class CrawlScheduler(
    object,
    metaclass = abc.ABCMeta,
):
    @property
    @abc.abstractmethod
    def pause_time_in_seconds(self) -> float:
        pass
