# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import locale
import scrapy
import pape.utilities
from newsbot.items import emailable_item_with_attachments


class MaineBreach(emailable_item_with_attachments.EmailableItemWithAttachments):
    organization_name = scrapy.Field()
    details_url = scrapy.Field()
    reported_date = scrapy.Field()
    
    org_type = scrapy.Field(ignore_when_serializing = True)
    people_affected = scrapy.Field(ignore_when_serializing = True)
    
    occurred_date = scrapy.Field(ignore_when_serializing = True)
    discovery_date = scrapy.Field(ignore_when_serializing = True)
    consumer_notification_date = scrapy.Field(ignore_when_serializing = True)
    
    breached_information = scrapy.Field(ignore_when_serializing = True)
    provided_description = scrapy.Field(ignore_when_serializing = True)
    
    submitter_name = scrapy.Field(ignore_when_serializing = True)
    submitter_relationship = scrapy.Field(ignore_when_serializing = True)
    submitter_email = scrapy.Field(ignore_when_serializing = True)
    submitter_phone_number = scrapy.Field(ignore_when_serializing = True)
    
    file_URLs = scrapy.Field(ignore_when_serializing = True)
    
    def __init__(self, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        super().__init__(*args, **kwargs)
    
    def synthesize_email_subject(self) -> str:
        return (
            f"{self['organization_name']} reports data breach"
            f" affecting {self._people_person_affected()}"
        )
    
    def _people_person_affected(self) -> str:
        try:
            return pape.utilities.pluralize(
                singular_form = "person",
                plural_form = "people",
                count = locale.atoi(self["people_affected"]),
            )
        except ValueError:
            return self["people_affected"]
    
    def synthesize_html_email_body(self) -> str:
        a_an_org_type = f"a {str.lower(self['org_type'])} organization"
        
        return self._get_email_template().safe_substitute({
            "email_subject": self.synthesize_email_subject(),
            "organization_name": self["organization_name"],
            "a_an_org_type": a_an_org_type,
            "details_url": self["details_url"],
            "people_person_affected": self._people_person_affected(),
            "occurred_date": self["occurred_date"],
            "discovery_date": self["discovery_date"],
            "consumer_notification_date": self["consumer_notification_date"],
            "reported_date": self["reported_date"],
            "breached_information": self["breached_information"],
            "provided_description": self["provided_description"],
            "submitter_name": self["submitter_name"],
            "submitter_relationship": self["submitter_relationship"],
            "submitter_email": self["submitter_email"],
            "submitter_phone_number": self["submitter_phone_number"],
            "consumer_notice_url": self["file_URLs"][0],
        })
