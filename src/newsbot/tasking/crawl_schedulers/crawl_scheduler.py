# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import abc


class CrawlScheduler(
    metaclass = abc.ABCMeta,
):
    @abc.abstractmethod
    def calculate_pause_time_in_seconds(self) -> float:
        pass
