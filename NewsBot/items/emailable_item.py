# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import string
import scrapy
import os
import pape


class EmailableItem(scrapy.Item):
    def get_email_subject(self) -> str:
        raise NotImplementedError
    
    def get_html_email_body(self) -> str:
        raise NotImplementedError
    
    def _get_attachment_paths(self) -> typing.Optional[typing.List[str]]:
        return None
    
    def get_email_attachments(self) -> [(str, (str, str))]:
        return [
            ("attachment", (
                os.path.basename(current_path),
                open(current_path, "rb").read()
            ))
            for current_path
            in self._get_attachment_paths() or []
        ]
    
    def _get_email_template(self, *,
        from_item_file_path: typing.AnyStr
    ) -> string.Template:
        item_file_path = from_item_file_path
        
        email_template_path = (
            os.path.abspath(
                os.path.join(
                    os.path.dirname(item_file_path),
                    f"""{
                        pape.utilities.strip_file_extension(
                            from_path = item_file_path,
                            basename_only = True,
                        )
                    }.template.html""",
                )
            )
        )
        
        return string.Template(open(email_template_path, "r").read())
