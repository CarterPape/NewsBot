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
        read_data=b"file content"
    )
    @unittest.mock.patch("newsbot.items.emailable_item_with_attachments.os.path.basename")
    def test_gather_email_attachments(self,
            mock_basename: unittest.mock.MagicMock,
            mock_open: unittest.mock.MagicMock,
        ):
        mock_basename.side_effect = lambda x: x.split("/")[-1]
        
        item = TestEmailableItemWithAttachments.MockEmailableItemWithAttachments()
        item["files"] = [{"path": "/path/to/file1.txt"}, {"path": "/path/to/file2.txt"}]
        
        expected_attachments = [
            ("attachment", ("file1.txt", b"file content")),
            ("attachment", ("file2.txt", b"file content"))
        ]
        
        attachments = item.gather_email_attachments()
        
        assert attachments == expected_attachments
        assert mock_open.call_count == 2
        mock_open.assert_any_call("/path/to/file1.txt", "rb")
        mock_open.assert_any_call("/path/to/file2.txt", "rb")
