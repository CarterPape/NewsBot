# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import os.path
import urllib.parse

import scrapy.http.request
import scrapy.http.response
import scrapy.pipelines.media
import scrapy.pipelines.files
import twisted.python.failure

from newsbot.items import item_with_files
from newsbot.item_pipelines import item_pipeline


class FileDownloader(
    scrapy.pipelines.files.FilesPipeline,
    item_pipeline.ItemPipeline,
):
    def file_path(self,
        request:    scrapy.http.request.Request,
        response:   scrapy.http.response.Response | None =                      None,
        info:       scrapy.pipelines.media.MediaPipeline.SpiderInfo | None =    None,
        *,
        item = None
    ) -> str:
        
        parsed_url =    urllib.parse.urlparse(request.url)
        return os.path.join(
            parsed_url.netloc.lstrip("/"),
            parsed_url.path.lstrip("/"),
        )
    
    def item_completed(self,
        results:    tuple[bool, (dict | twisted.python.failure.Failure)],
        item:       item_with_files.ItemWithFiles,
        info:       scrapy.pipelines.media.MediaPipeline.SpiderInfo,
    ):
        item = super().item_completed(results, item, info)
        
        for each_file in item[self.files_result_field]:
            each_file["path"] = os.path.abspath(
                os.path.join(
                    self.store.basedir,
                    each_file["path"]
                )
            )
        
        logging.debug(f"Files for item {item} downloaded")
        return item
