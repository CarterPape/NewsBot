# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import os.path
import abc

from newsbot.items import emailable_item
from newsbot.items import item_with_files


class EmailableItemWithAttachments(
    emailable_item.EmailableItem,
    item_with_files.ItemWithFiles,
    metaclass = abc.ABCMeta,
):
    def gather_email_attachments(self) -> typing.List[
        (str, (
            str,
            typing.IO[typing.Any]
        ))
    ]:
        return [
            ("attachment", (
                os.path.basename(current_file["path"]),
                open(current_file["path"], "rb").read()
            ))
            for current_file
            in self["files"] or []
        ]
