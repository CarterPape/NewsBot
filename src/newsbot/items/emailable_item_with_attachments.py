# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import mimetypes
import os.path
import io
import abc

from newsbot.items import emailable_item
from newsbot.items import item_with_files


class EmailableItemWithAttachments(
    emailable_item.EmailableItem,
    item_with_files.ItemWithFiles,
    metaclass = abc.ABCMeta,
):
    def gather_email_attachments(self) -> list[
        tuple[
            str, str, io.BufferedReader
        ]
    ]:
        return [
            (
                os.path.basename(current_file["path"]),
                mimetypes.guess_type(current_file["path"])[0] or "application/octet-stream",
                open(current_file["path"], "rb"),
            )
            for current_file
            in self["files"] or []
        ]
