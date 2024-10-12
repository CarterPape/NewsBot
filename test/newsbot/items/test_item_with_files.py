# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import unittest
from newsbot.items import item_with_files


class TestItemWithFiles(unittest.TestCase):
    def test_field_names(self):
        file_results_field = item_with_files.ItemWithFiles().get_files_result_field()
        file_urls_field = item_with_files.ItemWithFiles().get_files_urls_field()
        
        assert file_results_field != file_urls_field
        
        assert file_results_field in item_with_files.ItemWithFiles().fields
        assert file_urls_field in item_with_files.ItemWithFiles().fields
