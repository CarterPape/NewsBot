# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=invalid-name

from __future__ import annotations

import enum
import datetime
import typing
import zoneinfo

import dateparser

class DayOfTheWeek(enum.Flag):
    Monday =    enum.auto()
    Tuesday =   enum.auto()
    Wednesday = enum.auto()
    Thursday =  enum.auto()
    Friday =    enum.auto()
    Saturday =  enum.auto()
    Sunday =    enum.auto()
    
    weekdays =  Monday | Tuesday | Wednesday | Thursday | Friday
    weekends =  Saturday | Sunday
    
    @classmethod
    def from_datetime(klass,
        the_datetime: datetime.datetime,
    ) -> DayOfTheWeek:
        return klass.from_index_value(the_datetime.weekday())
    
    @classmethod
    def from_index_value(klass,
        index_value: int,
    ) -> DayOfTheWeek:
        return DayOfTheWeek(2 ** index_value)
    
    def next_day_of_the_week(self):
        next_day_index = (self.day_index + 1) % 7
        return DayOfTheWeek.from_index_value(next_day_index)
    
    def this_day_and_the_next_six_days(self):
        each_day = self
        for _ in range(7):
            yield each_day
            each_day = each_day.next_day_of_the_week()
    
    @property
    def day_index(self) -> int:
        if self.value.bit_count() != 1:
            raise ValueError(f"{self} is not an individual day of the week")
        
        return self.value.bit_length() - 1

class Time(datetime.time):
    def __new__(klass, time_string: str, *args, **kwargs):
        the_datetime = typing.cast(datetime.datetime,
            dateparser.parse(
                time_string,
                settings = {
                    'RETURN_AS_TIMEZONE_AWARE': False,
                },
            )
        )
        
        return super().__new__(klass,
            hour =          the_datetime.hour,
            minute =        the_datetime.minute,
            second =        the_datetime.second,
            microsecond =   the_datetime.microsecond,
            tzinfo =        None,
            *args, **kwargs
        )
    
    def on_date(self,
        the_date: datetime.date,
        *,
        in_timezone = zoneinfo.ZoneInfo("America/Denver"),
    ) -> datetime.datetime:
        return datetime.datetime.combine(the_date, self, in_timezone)

class IntervalRule:
    def __init__(self, *,
        start_time: Time,
        end_time:   Time,
        period:     datetime.timedelta,
    ):
        if end_time <= start_time:
            raise ValueError("The end time must be after the start time")
        
        if period <= datetime.timedelta(0):
            raise ValueError("The period must be greater than zero")
        
        common_time = datetime.date(2000, 1, 1)
        if period > (
            datetime.datetime.combine(common_time, end_time)
            - datetime.datetime.combine(common_time, start_time)
        ):
            raise ValueError("The period must be no longer than the interval")
        
        self.start_time =   start_time
        self.end_time =     end_time
        self.period =       period

FireRule = Time | IntervalRule

class WhenToFire(dict):
    def __getitem__(self,
        item: DayOfTheWeek,
    ) -> list[FireRule]:
        for key in self:
            if item in key:
                return super().__getitem__(key)
        return []
    
    def __contains__(self,
        item: DayOfTheWeek,
    ):
        for key in self:
            if item in key:
                return True
        return False

class NextFireDatetimeNotFound(Exception):
    pass
