# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import enum
import datetime
import typing
import math

import pytz
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
    ):
        return klass.from_index_value(the_datetime.weekday())
    
    @classmethod
    def from_index_value(klass,
        index_value: int,
    ):
        try:
            return klass._value2member_map_[2 ** index_value]
        except AttributeError as exception:
            raise AttributeError(
                "Looks like enum.Flag objects no longer have _value2member_map_ members."
            ) from exception
    
    def next_day_of_the_week(self):
        next_day_index = (self.day_index + 1) % 7
        return DayOfTheWeek.from_index_value(next_day_index)
    
    def this_day_and_the_next_six_days(self):
        for _ in range(7):
            yield self
            self = self.next_day_of_the_week()
    
    @property
    def day_index(self):
        day_index = math.log2(self.value)
        if not day_index.is_integer():
            raise ValueError(f"{self} is not an individual day of the week")
        
        return day_index

class Time(datetime.time):
    def __new__(klass, time_string: str):
        datetyme: datetime.datetime = dateparser.parse(
            time_string,
            settings = {
                'RETURN_AS_TIMEZONE_AWARE': False,
            },
        )
        
        return super().__new__(klass,
            hour =          datetyme.hour,
            minute =        datetyme.minute,
            second =        datetyme.second,
            microsecond =   datetyme.microsecond,
        )
    
    def on_date(self,
        the_date: datetime.date,
        *,
        in_timezone = pytz.timezone("America/Denver"),
    ) -> datetime.datetime:
        return datetime.datetime(
            year =          the_date.year,
            month =         the_date.month,
            day =           the_date.day,
            hour =          self.hour,
            minute =        self.minute,
            second =        self.second,
            microsecond =   self.microsecond,
            fold =          1,
        ).astimezone(in_timezone)

class IntervalRule(object):
    def __init__(self, *,
        start_time: Time,
        end_time:   Time,
        period:     datetime.timedelta,
    ):
        assert start_time < end_time
        self.start_time =   start_time
        self.end_time =     end_time
        self.period =       period

FireRule = typing.Union[
    Time,
    IntervalRule,
]

class WhenToFire(dict):
    def __getitem__(self,
        item: DayOfTheWeek,
    ) -> typing.List[FireRule]:
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

class NextFireDatetimeFound(Exception):
    pass
