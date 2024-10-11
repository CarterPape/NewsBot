# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import random
import typing

import zoneinfo

from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.tasking.crawl_schedulers.helpers import timing_types

_workday_when_to_fire = timing_types.WhenToFire({
    timing_types.DayOfTheWeek.weekdays: [
        timing_types.Time("12:00 a.m."),
        timing_types.Time("8:00 a.m."),
        timing_types.IntervalRule(
            start_time =    timing_types.Time("8:00 a.m."),
            end_time =      timing_types.Time("6:00 p.m."),
            period =        datetime.timedelta(minutes = 20),
        ),
        timing_types.Time("6:05 p.m."),
        timing_types.IntervalRule(
            start_time =    timing_types.Time("6:05 p.m."),
            end_time =      timing_types.Time("11:59:59 p.m."),
            period =        datetime.timedelta(hours = 3),
        ),
    ],
    timing_types.DayOfTheWeek.weekends: [
        timing_types.IntervalRule(
            start_time =    timing_types.Time("12:00 a.m."),
            end_time =      timing_types.Time("1:00 a.m."),
            period =        datetime.timedelta(hours = 1),
        ),
        timing_types.Time("1:00 a.m."),
        timing_types.Time("9:00 a.m."),
        timing_types.IntervalRule(
            start_time =    timing_types.Time("9:00 a.m."),
            end_time =      timing_types.Time("11:59:59 p.m."),
            period =        datetime.timedelta(hours = 1),
        ),
    ],
})

class TimeConditionalScheduler(crawl_scheduler.CrawlScheduler):
    def __init__(self, *,
        when_to_fire: timing_types.WhenToFire = _workday_when_to_fire,
        working_timezone: datetime.tzinfo =     zoneinfo.ZoneInfo("America/Denver"),
        uniform_relative_deviation =            0.1,
        uniform_absolute_deviation =            datetime.timedelta(minutes = 10),
        datetime_of_previous_firing: (datetime.datetime | None) = None,
    ):
        self._working_timezone =            working_timezone
        self._when_to_fire =                when_to_fire
        self._uniform_relative_deviation =  uniform_relative_deviation
        self._uniform_absolute_deviation =  uniform_absolute_deviation
        
        # In cases where the datetime of the previous firing is not set, assuming it to be the current datetime ensures that the scheduler schedules the next firing as though the most recent firing just happened, because it might have, and even if it didn't, we still don't want to fire too often.
        # Once the first scheduled pause time is calculated, _datetime_of_previous_firing will become the actual time of the most recent firing.
        self._datetime_of_previous_firing:          datetime.datetime = \
            datetime_of_previous_firing or datetime.datetime.now(tz = self._working_timezone)
        self._datetime_of_next_firing:              datetime.datetime | None = None
    
    @classmethod
    def _now(klass) -> datetime.datetime:
        return datetime.datetime.now(tz = zoneinfo.ZoneInfo("America/Denver")) # pragma: no cover
    
    def calculate_pause_time_in_seconds(self) -> float:
        self._find_next_fire_datetime()
        
        if self._datetime_of_next_firing is None:
            raise timing_types.NextFireDatetimeNotFound(
                f"The next fire time for {self._when_to_fire} was not found "
                f"based on the previous fire time of {self._datetime_of_previous_firing}. "
                f"This should only happen if the WhenToFire is empty."
            )
        
        now = TimeConditionalScheduler._now()
        
        self._datetime_of_next_firing = max(
            typing.cast(datetime.datetime, self._datetime_of_next_firing),
            now,
        )
        
        self._datetime_of_previous_firing = self._datetime_of_next_firing
        
        return (self._datetime_of_next_firing - now).total_seconds()
    
    def _find_next_fire_datetime(self):
        self._datetime_of_next_firing = None
        
        start_day_of_the_week = timing_types.DayOfTheWeek.from_datetime(
            self._datetime_of_previous_firing
        )
        
        for each_day_of_the_week in start_day_of_the_week.this_day_and_the_next_six_days():
            each_date = self._current_or_next_future_date_from(
                day_of_the_week = each_day_of_the_week
            )
            
            for each_fire_rule in self._when_to_fire[each_day_of_the_week]:
                if issubclass(type(each_fire_rule), timing_types.Time):
                    self._handle_time_fire_rule(
                        typing.cast(timing_types.Time, each_fire_rule),
                        on_date = each_date,
                    )
                else:
                    self._handle_interval_fire_rule(
                        typing.cast(timing_types.IntervalRule, each_fire_rule),
                        on_date = each_date,
                    )
                
                if self._datetime_of_next_firing is not None:
                    return
    
    def _handle_time_fire_rule(self,
        the_time: timing_types.Time,
        *,
        on_date: datetime.date
    ):
        the_date = on_date
        potential_datetime_of_next_firing = the_time.on_date(the_date)
        if self._datetime_of_previous_firing <= potential_datetime_of_next_firing:
            self._datetime_of_next_firing = self._datetime_with_absolute_random_deviation(
                potential_datetime_of_next_firing
            )
            return
        else:
            assert potential_datetime_of_next_firing < self._datetime_of_previous_firing
            return
    
    def _handle_interval_fire_rule(self,
        the_interval_fire_rule: timing_types.IntervalRule,
        *,
        on_date: datetime.date
    ):
        the_date = on_date
        interval_start_datetime = the_interval_fire_rule.start_time.on_date(the_date)
        interval_end_datetime = the_interval_fire_rule.end_time.on_date(the_date)
        
        if self._datetime_of_previous_firing <= interval_start_datetime:
            self._datetime_of_next_firing = (
                interval_start_datetime
                + self._period_with_relative_random_deviation(the_interval_fire_rule.period)
            )
        elif self._datetime_of_previous_firing <= interval_end_datetime:
            potential_datetime_of_next_firing = (
                self._datetime_of_previous_firing
                + self._period_with_relative_random_deviation(the_interval_fire_rule.period)
            )
            if potential_datetime_of_next_firing <= interval_end_datetime:
                self._datetime_of_next_firing = potential_datetime_of_next_firing
            else:
                assert interval_end_datetime < potential_datetime_of_next_firing
        else:
            assert interval_end_datetime < self._datetime_of_previous_firing
    
    def _current_or_next_future_date_from(self, *,
        day_of_the_week: timing_types.DayOfTheWeek,
    ) -> datetime.date:
        days_until_the_day_of_the_week = datetime.timedelta(
            days = (
                day_of_the_week.day_index - self._datetime_of_previous_firing.weekday()
            ) % 7
        )
        return (self._datetime_of_previous_firing + days_until_the_day_of_the_week).date()
    
    def _datetime_with_absolute_random_deviation(self,
        the_datetime: datetime.datetime,
    ) -> datetime.datetime:
        return the_datetime + (
            self._uniform_absolute_deviation * random.uniform(0, 1)
        )
    
    def _period_with_relative_random_deviation(self,
        period: datetime.timedelta,
    ) -> datetime.timedelta:
        return period * random.Random().uniform(
            1 - self._uniform_relative_deviation,
            1 + self._uniform_relative_deviation,
        )
