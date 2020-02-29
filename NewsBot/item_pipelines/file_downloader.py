# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.pipelines.files
import os.path
import urllib.parse
import twisted.python.failure
import typing
import newsbot.items.item_with_files as item_with_files
import newsbot.item_pipelines.item_pipeline as item_pipeline


class FileDownloader(
    scrapy.pipelines.files.FilesPipeline,
    item_pipeline.ItemPipeline,
):
    def file_path(self,
        request:    scrapy.http.Request,
        response:   scrapy.http.Response =                              None,
        info:       scrapy.pipelines.media.MediaPipeline.SpiderInfo =   None,
    ) -> str:
        
        parsed_url =    urllib.parse.urlparse(request.url)
        return os.path.join(
            parsed_url.netloc.lstrip("/"),
            parsed_url.path.lstrip("/"),
        )
    
    def item_completed(self,
        results:    (bool, typing.Union[dict, twisted.python.failure.Failure]),
        item:       item_with_files.ItemWithFiles,
        info:       scrapy.pipelines.media.MediaPipeline.SpiderInfo,
    ):
        item = super().item_completed(results, item, info)
        
        for fyle in item[self.files_result_field]:
            fyle["path"] = os.path.abspath(
                os.path.join(
                    self.store.basedir,
                    fyle["path"]
                )
            )
        return item
