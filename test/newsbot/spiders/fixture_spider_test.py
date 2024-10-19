# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import os
import abc
import unittest
import datetime
import logging

import scrapy.utils.conf

import requests_cache

from newsbot.spiders import self_scheduling_spider

class SpiderTestCase(
    unittest.TestCase,
    metaclass=abc.ABCMeta,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spider: self_scheduling_spider.SelfSchedulingSpider
    
    def _page_snapshot_path(self, *, from_relative_filename: str) -> str:
        return (
            os.path.join(
                os.path.abspath(
                    os.path.dirname(
                        scrapy.utils.conf.closest_scrapy_cfg(
                            path = os.path.realpath(__file__)
                        )
                    )
                ),
                from_relative_filename,
            )
        )
    
    def _retrieve_possibly_cached_page_body(self, *,
        url: str,
        data: dict[str, str] | None = None,
        method: str = "GET",
    ) -> str:
        cached_session = requests_cache.CachedSession(
            backend = requests_cache.FileCache("test/test_data/requests_cache"),
            expire_after = datetime.timedelta(days = 1),
            allowable_methods = ["GET", "POST", "HEAD"],
        )
        
        response = cached_session.request(
            method = method,
            url = url,
            data = data,
        )
        if response.from_cache:
            logging.info(f"Returning cached page at {url}")
        else:
            logging.info(f"Returning live page at {url}")
        
        return response.text
    
    def test_spider_class_has_name(self):
        self.assertIsNotNone(self.spider.name)
