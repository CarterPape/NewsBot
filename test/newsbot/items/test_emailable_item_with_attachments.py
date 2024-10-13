# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import unittest.mock
from newsbot.items import emailable_item_with_attachments


class TestEmailableItemWithAttachments(unittest.TestCase):
    class MockEmailableItemWithAttachments(
        emailable_item_with_attachments.EmailableItemWithAttachments
    ):
        def synthesize_email_subject(self):
            return "Email subject"
        def synthesize_html_email_body(self):
            return "Email body"
    
    @unittest.mock.patch(
        "newsbot.items.emailable_item_with_attachments.open",
        new_callable=unittest.mock.mock_open,
        read_data=b"file content",
    )
    def test_gather_email_attachments(self,
            mock_open: unittest.mock.MagicMock,
        ):
        def simplified_basename(path: str) -> str:
            return path.split("/")[-1]
        
        item = TestEmailableItemWithAttachments.MockEmailableItemWithAttachments()
        item["files"] = [
            {"path": "/fake/absolute/path/to/file1.txt"},
            {"path": "relative/path/to/file2.txt"}
        ]
        
        expected_attachments = [
            ("attachment", (simplified_basename(item["files"][0]["path"]), b"file content")),
            ("attachment", (simplified_basename(item["files"][1]["path"]), b"file content"))
        ]
        
        attachments = item.gather_email_attachments()
        
        assert attachments == expected_attachments
        assert mock_open.call_count == 2
        mock_open.assert_any_call(item["files"][0]["path"], "rb")
        mock_open.assert_any_call(item["files"][1]["path"], "rb")
