# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import pytest

from newsbot.tasking.crawl_schedulers.helpers import timing_types

def test_day_of_the_week_from_datetime():
    dt = datetime.datetime(2023, 10, 2)
    
    assert timing_types.DayOfTheWeek.from_datetime(dt) == timing_types.DayOfTheWeek.Monday

def test_day_of_the_week_from_index_value():
    assert timing_types.DayOfTheWeek.from_index_value(0) == timing_types.DayOfTheWeek.Monday
    assert timing_types.DayOfTheWeek.from_index_value(6) == timing_types.DayOfTheWeek.Sunday

def test_day_of_the_week_next_day():
    assert timing_types.DayOfTheWeek.Monday.next_day_of_the_week() == \
        timing_types.DayOfTheWeek.Tuesday
    assert timing_types.DayOfTheWeek.Sunday.next_day_of_the_week() == \
        timing_types.DayOfTheWeek.Monday

def test_day_of_the_week_this_day_and_the_next_six_days():
    days = list(
        timing_types.DayOfTheWeek.Friday.this_day_and_the_next_six_days()
    )
    
    assert days == [
        timing_types.DayOfTheWeek.Friday,
        timing_types.DayOfTheWeek.Saturday,
        timing_types.DayOfTheWeek.Sunday,
        timing_types.DayOfTheWeek.Monday,
        timing_types.DayOfTheWeek.Tuesday,
        timing_types.DayOfTheWeek.Wednesday,
        timing_types.DayOfTheWeek.Thursday,
    ]

def test_day_of_the_week_day_index_bad():
    with pytest.raises(ValueError, match="is not an individual day of the week"):
        _ = timing_types.DayOfTheWeek.weekdays.day_index

def test_time_creation():
    time = timing_types.Time("2:30 p.m.")
    
    assert time.hour == 14
    assert time.minute == 30
    assert time.second == 0
    assert time.tzinfo is None

def test_time_on_date():
    time = timing_types.Time("12:30 p.m.")
    date = datetime.date(2023, 10, 2)
    dt = time.on_date(date)
    
    assert dt.year == 2023
    assert dt.month == 10
    assert dt.day == 2
    assert dt.hour == 12
    assert dt.minute == 30
    assert dt.second == 0
    assert str(dt.tzinfo) == "America/Denver"

def test_interval_rule():
    start_time = timing_types.Time("9:00 a.m.")
    end_time = timing_types.Time("5 p.m.")
    period = datetime.timedelta(hours = 1)
    rule = timing_types.IntervalRule(
        start_time = start_time,
        end_time = end_time,
        period = period
    )
    
    assert rule.start_time == start_time
    assert rule.end_time == end_time
    assert rule.period == period

def test_bad_interval_rules():
    with pytest.raises(ValueError, match="The end time must be after the start time"):
        timing_types.IntervalRule(
            start_time = timing_types.Time("9:00 a.m."),
            end_time = timing_types.Time("8:59 a.m."),
            period = datetime.timedelta(hours = 1)
        )
    
    with pytest.raises(ValueError, match="The end time must be after the start time"):
        timing_types.IntervalRule(
            start_time = timing_types.Time("9:00 a.m."),
            end_time = timing_types.Time("9:00 a.m."),
            period = datetime.timedelta(minutes = 1)
        )
    
    with pytest.raises(ValueError, match="The period must be greater than zero"):
        timing_types.IntervalRule(
            start_time = timing_types.Time("9:00 a.m."),
            end_time = timing_types.Time("5 p.m."),
            period = datetime.timedelta(minutes = 0)
        )
    
    with pytest.raises(ValueError, match="The period must be no longer than the interval"):
        timing_types.IntervalRule(
            start_time = timing_types.Time("9:00 a.m."),
            end_time = timing_types.Time("10 a.m."),
            period = datetime.timedelta(hours = 2)
        )

def test_when_to_fire():
    when_to_fire = timing_types.WhenToFire()
    when_to_fire[timing_types.DayOfTheWeek.Monday] = [timing_types.Time("9 p.m.")]
    
    assert timing_types.DayOfTheWeek.Monday in when_to_fire
    assert timing_types.DayOfTheWeek.Tuesday not in when_to_fire
    assert when_to_fire[timing_types.DayOfTheWeek.Monday] == [timing_types.Time("9 p.m.")]

def test_next_fire_datetime_not_found():
    with pytest.raises(timing_types.NextFireDatetimeNotFound):
        raise timing_types.NextFireDatetimeNotFound()
