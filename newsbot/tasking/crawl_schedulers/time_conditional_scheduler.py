# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import random

import pytz

from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.tasking.crawl_schedulers.helpers.timing_types import \
    DayOfTheWeek, Time, IntervalRule, WhenToFire, NextFireDatetimeFound

_workday_when_to_fire = WhenToFire({
    DayOfTheWeek.weekdays: [
        Time("12:00 a.m."),
        Time("8:00 a.m."),
        IntervalRule(
            start_time =    Time("8:00 a.m."),
            end_time =      Time("6:00 p.m."),
            period =        datetime.timedelta(minutes = 20),
        ),
        Time("6:05 p.m."),
        IntervalRule(
            start_time =    Time("6:00 p.m."),
            end_time =      Time("11:59:59 p.m."),
            period =        datetime.timedelta(hours = 3),
        ),
    ],
    DayOfTheWeek.weekends: [
        IntervalRule(
            start_time =    Time("12:00 a.m."),
            end_time =      Time("1:00 a.m."),
            period =        datetime.timedelta(hours = 1),
        ),
        Time("1:00 a.m."),
        Time("9:00 a.m."),
        IntervalRule(
            start_time =    Time("9:00 a.m."),
            end_time =      Time("11:59:59 p.m."),
            period =        datetime.timedelta(hours = 1),
        ),
    ],
})

class TimeConditionalScheduler(crawl_scheduler.CrawlScheduler):
    def __init__(self, *,
        when_to_fire: WhenToFire =          _workday_when_to_fire,
        working_timezone: datetime.tzinfo = pytz.timezone("America/Denver"),
        uniform_relative_deviation =        0.1,
        uniform_absolute_deviation =        datetime.timedelta(minutes = 10),
    ):
        self._working_timezone =            working_timezone
        self._when_to_fire =                when_to_fire
        self._uniform_relative_deviation =  uniform_relative_deviation
        self._uniform_absolute_deviation =  uniform_absolute_deviation
        
        self._datetime_of_previous_firing:          datetime.datetime = \
            datetime.datetime.now(tz = self._working_timezone)
        self._now:                                  datetime.datetime = None
        self._datetime_of_next_firing:              datetime.datetime = None
        self._potential_datetime_of_next_firing:    datetime.datetime = None
    
    @property
    def pause_time_in_seconds(self) -> float:
        self._now =                                 self._datetime_of_previous_firing
        self._datetime_of_next_firing =             None
        self._potential_datetime_of_next_firing =   None
        
        try:
            self._find_next_fire_datetime()
        except NextFireDatetimeFound:
            pass
        
        if self._datetime_of_next_firing is None:
            self._datetime_of_next_firing = self._potential_datetime_of_next_firing
        
        true_now = datetime.datetime.now(tz = self._working_timezone)
        
        self._datetime_of_next_firing = max(
            self._datetime_of_next_firing,
            true_now,
        )
        
        self._datetime_of_previous_firing = self._datetime_of_next_firing
        
        return (self._datetime_of_next_firing - true_now).total_seconds()
    
    def _find_next_fire_datetime(self):
        current_day_of_the_week =       DayOfTheWeek.from_datetime(self._now)
        
        for each_day_of_the_week in current_day_of_the_week.this_day_and_the_next_six_days():
            the_day_of_the_week = each_day_of_the_week
            the_date = self._current_or_next_future_date_from(day_of_the_week = the_day_of_the_week)
            
            for each_fire_rule in self._when_to_fire[the_day_of_the_week]:
                the_fire_rule = each_fire_rule
                if issubclass(type(the_fire_rule), Time):
                    self._handle_time_fire_rule(
                        the_fire_rule,
                        on_date = the_date,
                    )
                else:
                    self._handle_interval_fire_rule(
                        the_fire_rule,
                        on_date = the_date,
                    )
            
            if self._potential_datetime_of_next_firing:
                self._datetime_of_next_firing = self._potential_datetime_of_next_firing
                return
            else:
                assert self._potential_datetime_of_next_firing is None
                continue
    
    def _handle_time_fire_rule(self,
        the_time: Time,
        *,
        on_date: datetime.date
    ):
        the_date = on_date
        the_datetime = the_time.on_date(the_date)
        if self._now <= the_datetime:
            if self._potential_datetime_of_next_firing is None:
                self._datetime_of_next_firing = self._datetime_with_random_deviation(
                    the_datetime
                )
                raise NextFireDatetimeFound()
            else:
                assert self._potential_datetime_of_next_firing is not None
                if the_datetime <= self._potential_datetime_of_next_firing:
                    self._datetime_of_next_firing = self._datetime_with_random_deviation(
                        the_datetime
                    )
                    raise NextFireDatetimeFound()
                else:
                    assert self._potential_datetime_of_next_firing < the_datetime
                    return
        else:
            assert the_datetime <= self._now
            return
    
    def _handle_interval_fire_rule(self,
        the_interval_fire_rule: IntervalRule,
        *,
        on_date: datetime.date
    ):
        the_date = on_date
        interval_start_datetime = the_interval_fire_rule.start_time.on_date(the_date)
        interval_end_datetime = the_interval_fire_rule.end_time.on_date(the_date)
        
        if self._potential_datetime_of_next_firing is not None:
            if self._potential_datetime_of_next_firing < interval_start_datetime:
                return
            
        if self._now <= interval_end_datetime:
            self._potential_datetime_of_next_firing = (
                self._now
            ) + (
                self._period_with_random_deviation(the_interval_fire_rule.period)
            )
            if interval_end_datetime <= self._potential_datetime_of_next_firing:
                self._potential_datetime_of_next_firing = None
                return
            elif self._potential_datetime_of_next_firing < interval_start_datetime:
                self._potential_datetime_of_next_firing = self._datetime_with_random_deviation(
                    interval_start_datetime
                )
            else:
                assert interval_start_datetime <= self._potential_datetime_of_next_firing
                assert self._potential_datetime_of_next_firing < interval_end_datetime
                return
        else:
            assert interval_end_datetime < self._now
            return
    
    def _current_or_next_future_date_from(self, *,
        day_of_the_week: DayOfTheWeek,
    ) -> datetime.date:
        time_until_the_day_of_the_week = datetime.timedelta(
            days = (
                day_of_the_week.day_index - self._now.weekday()
            ) % 7
        )
        return self._now + time_until_the_day_of_the_week
    
    def _datetime_with_random_deviation(self,
        datetyme: datetime.datetime,
    ) -> datetime.datetime:
        return datetyme + (
            self._uniform_absolute_deviation * random.uniform(0, 1)
        )
    
    def _period_with_random_deviation(self,
        period: datetime.timedelta,
    ) -> datetime.timedelta:
        return period * random.uniform(
            1 - self._uniform_relative_deviation,
            1 + self._uniform_relative_deviation,
        )
