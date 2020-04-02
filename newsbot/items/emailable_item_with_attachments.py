# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import string
import scrapy
import os.path
import pape
import newsbot.items.emailable_item as emailable_item
import newsbot.items.item_with_files as item_with_files
import abc


class EmailableItemWithAttachments(
    emailable_item.EmailableItem,
    item_with_files.ItemWithFiles,
    metaclass = abc.ABCMeta,
):
    def gather_email_attachments(self) -> [(str, (str, typing.IO[typing.Any]))]:
        return [
            ("attachment", (
                os.path.basename(current_file["path"]),
                open(current_file["path"], "rb").read()
            ))
            for current_file
            in self["files"] or []
        ]
