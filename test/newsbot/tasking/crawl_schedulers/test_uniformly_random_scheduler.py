# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import datetime
import unittest.mock

import pytest

from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler

@unittest.mock.patch("random.Random.random")
def test_calculate_pause_time_in_seconds(mock_random: unittest.mock.MagicMock):
    mock_random.return_value = 0.5
    min_interval = datetime.timedelta(seconds=0)
    max_interval = datetime.timedelta(seconds=20)
    scheduler = uniformly_random_scheduler.UniformlyRandomScheduler(
        minimum_interval=min_interval,
        maximum_interval=max_interval,
        first_call_is_immediate=True
    )
    
    assert scheduler.calculate_pause_time_in_seconds() == 0
    assert scheduler.calculate_pause_time_in_seconds() == 10

def test_init_with_invalid_interval():
    min_interval = datetime.timedelta(seconds=20)
    max_interval = datetime.timedelta(seconds=10)
    
    with pytest.raises(
        AssertionError,
        match="minimum_interval must be less than or equal to maximum_interval"
    ):
        uniformly_random_scheduler.UniformlyRandomScheduler(
            minimum_interval=min_interval,
            maximum_interval=max_interval
        )
