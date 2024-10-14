# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access
# type: ignore
# pylint: disable=useless-parent-delegation
# pylint: disable=abstract-class-instantiated

import string
import unittest
import unittest.mock

import pytest

from newsbot.items.emailable_item import EmailableItem

class MockEmailableItem(EmailableItem):
    def synthesize_email_subject(self) -> str:
        return super().synthesize_email_subject()
    
    def synthesize_html_email_body(self) -> str:
        return super().synthesize_html_email_body()

class TestEmailableItem(unittest.TestCase):
    @unittest.mock.patch(
        "newsbot.items.emailable_item.open",
        new_callable=unittest.mock.mock_open,
        read_data="fake file $content"
    )
    def test_get_email_template(self, _):
        template = MockEmailableItem()._get_email_template()
        
        assert isinstance(template, string.Template)
        assert template.template == "fake file $content"
    
    def test_synthesize_email_subject(self):
        with pytest.raises(
            NotImplementedError,
            match = "MockEmailableItem.synthesize_email_subject is not defined"
        ):
            MockEmailableItem().synthesize_email_subject()
    
    def test_synthesize_html_email_body(self):
        with pytest.raises(
            NotImplementedError,
            match = "MockEmailableItem.synthesize_html_email_body is not defined"
        ):
            MockEmailableItem().synthesize_html_email_body()
