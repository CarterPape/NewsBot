# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import datetime
import copy
import unittest.mock
import pytest
import dateparser

from newsbot.tasking.crawl_schedulers import time_conditional_scheduler
from newsbot.tasking.crawl_schedulers.helpers import timing_types

@unittest.mock.patch("random.Random.random")
class TestTimeConditionalScheduler(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        example_datetime = dateparser.parse(
            "Monday, October 2, 2023 at 1:30 p.m.",
            settings = {
                "TIMEZONE": "America/Denver",
                "RETURN_AS_TIMEZONE_AWARE": True,
            },
        )
        assert example_datetime is not None
        
        self.example_datetime: datetime.datetime = example_datetime
        self.common_scheduler = time_conditional_scheduler.TimeConditionalScheduler(
            datetime_of_previous_firing = self.example_datetime,
        )
        
        super().__init__(*args, **kwargs)
    
    def test_calculate_pause_time_in_seconds(self, mock_random: unittest.mock.MagicMock):
        assert False
    
    def test_calculate_pause_time_in_seconds_with_bad_rules(
            self, mock_random: unittest.mock.MagicMock
        ):
        empty_scheduler = time_conditional_scheduler.TimeConditionalScheduler(
            when_to_fire = timing_types.WhenToFire({}),
            datetime_of_previous_firing = self.example_datetime,
        )
        mock_random.return_value = 0
        
        with pytest.raises(timing_types.NextFireDatetimeNotFound):
            empty_scheduler.calculate_pause_time_in_seconds()
    
    def test_find_next_fire_datetime(self, mock_random: unittest.mock.MagicMock):
        assert False
        
    def test_handle_time_fire_rule(self, mock_random: unittest.mock.MagicMock):
        inputs_and_expected_value_list: list[tuple[
            timing_types.Time, float, (datetime.datetime | None)
        ]] = [
            (timing_types.Time("1:30 a.m."), 0.5, None),
            (timing_types.Time("1:29:59 p.m."), 0, None),
            (timing_types.Time("1:30:00 p.m."), 0.5, (
                self.example_datetime + datetime.timedelta(minutes = 5)
            )),
            (timing_types.Time("1:31 p.m."), 1, (
                self.example_datetime + datetime.timedelta(minutes = 11)
            )),
            (timing_types.Time("11:59:59 p.m."), 0, (
                self.example_datetime + datetime.timedelta(hours = 10, minutes = 29, seconds = 59)
            )),
        ]
        
        for time_rule, random_value, expected_datetime_of_next_firing \
            in inputs_and_expected_value_list:
            the_scheduler = copy.copy(self.common_scheduler)
            mock_random.return_value = random_value
            the_scheduler._handle_time_fire_rule(
                time_rule,
                on_date = self.example_datetime.date()
            )
            
            assert the_scheduler._datetime_of_next_firing == expected_datetime_of_next_firing
        
    def test_handle_interval_fire_rule(self, mock_random: unittest.mock.MagicMock):
        pass
    
    def test_current_or_next_future_date(self, _: unittest.mock.MagicMock):
        assert self.common_scheduler._current_or_next_future_date_from(
                day_of_the_week = timing_types.DayOfTheWeek.Monday
            ) == self.example_datetime.date()
        
        assert self.common_scheduler._current_or_next_future_date_from(
                day_of_the_week = timing_types.DayOfTheWeek.Sunday
            ) == (self.example_datetime.date() + datetime.timedelta(days = 6))
    
    def test_datetime_with_absolute_random_deviation(self, mock_random: unittest.mock.MagicMock):
        random_value_and_expected_offset_list = [
            (0,     0),
            (0.25,  2.5),
            (0.5,   5),
            (0.9,   9),
            (1,     10),
        ]
        
        for random_value, expected_offset in random_value_and_expected_offset_list:
            mock_random.return_value = random_value
            deviation = self.common_scheduler._datetime_with_absolute_random_deviation(
                self.example_datetime
            )
            assert deviation == (
                self.example_datetime
                + datetime.timedelta(minutes = expected_offset)
            )
    
    def test_period_with_relative_random_deviation(self, mock_random: unittest.mock.MagicMock):
        random_value_and_expected_deviation_list = [
            (0,     90),
            (0.25,  95),
            (0.5,   100),
            (0.8,   106),
            (1,     110),
        ]
        
        for random_value, expected_deviation in random_value_and_expected_deviation_list:
            mock_random.return_value = random_value
            deviation = self.common_scheduler._period_with_relative_random_deviation(
                datetime.timedelta(seconds = 100)
            )
            assert deviation == datetime.timedelta(seconds = expected_deviation)
