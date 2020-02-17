# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.item
import scrapy.exceptions
import NewsBot.settings
import NewsBot.items.item_with_files
import NewsBot.spiders
import os.path
import urllib.parse
import logging
import twisted.internet.defer
import typing


class FileDownloader(
    scrapy.pipelines.files.FilesPipeline,
    NewsBot.item_pipelines.item_pipeline.ItemPipeline,
):
    _DOWNLOAD_DIRECTORY = os.path.join(
        NewsBot.settings._DATA_DIRECTORY,
        "file-downloads/"
    )
    
    def __init__(self,
        store_uri:      str,
        download_func:  typing.Callable =           None,
        settings:       scrapy.settings.Settings =  None,
    ):
        self.FILES_URLS_FIELD = (
            NewsBot.items.item_with_files.ItemWithFiles.get_files_urls_field()
        )
        self.FILES_RESULT_FIELD = (
            NewsBot.items.item_with_files.ItemWithFiles.get_files_result_field()
        )
        
        super().__init__(
            store_uri,
            download_func = download_func,
            settings =      settings
        )
    
    def file_path(self,
        request:    scrapy.http.Request,
        response:   scrapy.http.Response =                              None,
        info:       scrapy.pipelines.media.MediaPipeline.SpiderInfo =   None,
    ) -> str:
        parsed_url =    urllib.parse.urlparse(request.url)
        return os.path.join(
            self._DOWNLOAD_DIRECTORY,
            parsed_url.netloc.lstrip("/"),
            parsed_url.path.lstrip("/"),
        )
