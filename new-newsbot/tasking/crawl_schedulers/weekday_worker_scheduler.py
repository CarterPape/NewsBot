# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import newsbot.tasking.crawl_schedulers.crawl_scheduler as crawl_scheduler
import random
import pytz

[
    "12:05 a.m.",
    "8:05 a.m.",
    {
        "start":    "8:00 a.m.",
        "end":      "6:00 p.m.",
        "interval": "every 20 minutes",
    },
    "6:10 p.m.",
    {
        "start":    "6:00 p.m.",
        "end":      "12:00 a.m.",
        "interval": "every 3 hours",
    },
]

class WeekdayWorkerScheduler(crawl_scheduler.CrawlScheduler):
    def __init__(self, *,
        average_check_interval_during_workday = datetime.timedelta(minutes = 20),
        average_check_interval_after_hours =    datetime.timedelta(hours = 4),
        average_check_interval_while_asleep =   None,
        average_check_interval_during_weekend = datetime.timedelta(hours = 8),
        
        uniform_relative_deviation =            0.1,
        
        source_timezone =                       pytz.timezone("America/Denver"),
        workday_start_time =                    datetime.timedelta(hours = 8),
        workday_end_time =                      datetime.timedelta(hours = 18),
        bed_time =                              datetime.timedelta(hours = 0),
        wake_up_time =                          datetime.timedelta(hours = 6),
    ):
        self._average_check_interval_during_workday =   average_check_interval_during_workday
        self._average_check_interval_after_hours =      average_check_interval_after_hours
        self._average_check_interval_during_weekend =   average_check_interval_during_weekend
        
        self._uniform_relative_deviation =              uniform_relative_deviation
        
        self._source_timezone =     source_timezone
        self._workday_start_time =  workday_start_time
        self._workday_end_time =    workday_end_time
        self._bed_time =            bed_time
        self._wake_up_time =        wake_up_time
        
        self._now = datetime.datetime.now(tz = self._source_timezone)
    
    @property
    def upcoming_midnight(self) -> datetime.datetime:
        tomorrow = self._now + datetime.timedelta(days = 1)
        
        return tomorrow.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0,
        )
    
    @property
    def pause_time_in_seconds(self):
        self._now = datetime.datetime.now(tz = self._source_timezone)
        
        if self.at_work_now:
            pass
        elif self.after_hours_now:
            pass
        elif self.asleep_now:
            pass
        elif self.morning_hours_now:
            pass
        
        return (
            random.uniform(
                self._minimum_interval,
                self._maximum_interval,
            ).total_seconds()
        )
