# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access


import datetime
import unittest.mock
import string

from newsbot.items import dispatch


class TestDispatch(unittest.TestCase):
    def setUp(self):
        self.dispatch_instance = dispatch.Dispatch()
        self.dispatch_instance['dispatched_agency'] = 'Fire Department'
        self.dispatch_instance['datetime_dispatched'] = datetime.datetime(2023, 10, 5, 14, 30)
        self.dispatch_instance['files'] = [{'url': 'http://example.com/audio.mp3'}]
        
    def test_synthesize_email_subject(self):
        expected_subject = "Call to Fire Department Thursday at 2:30 PM"
        assert self.dispatch_instance.synthesize_email_subject() == expected_subject

    @unittest.mock.patch.object(dispatch.Dispatch, '_get_email_template')
    def test_synthesize_html_email_body(self, mock_get_email_template):
        template_string = string.Template(
            "<html><body><h1>${email_subject}</h1><p>Dispatched at ${dispatch_time} on "
            "${dispatch_date} to ${dispatched_agency}. Audio: ${dispatch_audio_url}"
            "</p></body></html>"
        )
        mock_get_email_template.return_value = template_string

        expected_body = (
            "<html><body><h1>Call to Fire Department Thursday at 2:30 PM</h1>"
            "<p>Dispatched at 14:30:00 on Thursday, Oct.  5 to Fire Department. "
            "Audio: http://example.com/audio.mp3</p></body></html>"
        )
        assert self.dispatch_instance.synthesize_html_email_body() == expected_body
