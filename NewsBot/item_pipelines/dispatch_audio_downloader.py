# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.exceptions
import NewsBot.settings
import NewsBot.items
import NewsBot.spiders
import os.path
import urllib.parse
import logging

class DispatchAudioDownloader(object):
    _DOWNLOAD_DIRECTORY = os.path.join(NewsBot.settings._DATA_DIRECTORY, "dispatch-audio/")
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    
    def process_item(
        self,
        item: NewsBot.items.Dispatch,
        spider: NewsBot.spiders.DispatchCallLogSpider
    ):
        item["audio_file_path"] = self._save_location(of_dispatch = item)
        
        if self._audio_already_downloaded(of_dispatch = item):
            self._logger.info(f"{item['audio_file_path']} already exists")
            raise scrapy.exceptions.DropItem
        
        request = scrapy.Request(item["audio_URL"])
        download_deferred = spider.crawler.engine.download(request, spider)
        download_deferred.addBoth(self._handle_item_downloaded, item)
        self._logger.info(f"downloading {item['audio_URL']} to {item['audio_file_path']}")
        return download_deferred
    
    def _handle_item_downloaded(
        self,
        response: scrapy.http.Response,
        item: NewsBot.items.Dispatch
    ):
        if response.status != 200:
            self._logger.warn(
                f"Got HTML code {response.status} looking for {response.url}. "
                "Dropping associated item."
            )
            raise scrapy.exceptions.DropItem
        
        os.makedirs(os.path.dirname(item["audio_file_path"]), exist_ok = True)
        with open(item["audio_file_path"], "xb") as audio_file:
            self._logger.info(f"downloading {item['audio_URL']} to {item['audio_file_path']}")
            audio_file.write(response.body)
        
        return item
    
    def _save_location(self, *, of_dispatch: NewsBot.items.Dispatch):
        dispatch    = of_dispatch
        parsed_url  = urllib.parse.urlparse(dispatch["audio_URL"])
        return os.path.join(
            self._DOWNLOAD_DIRECTORY,
            parsed_url.netloc,
            parsed_url.path.lstrip("/"),
        )
    
    def _audio_already_downloaded(self, *, of_dispatch: NewsBot.items.Dispatch):
        dispatch = of_dispatch
        return os.path.exists(dispatch["audio_file_path"])
