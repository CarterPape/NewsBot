# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import newsbot.items.emailable_item_with_attachments as emailable_item_with_attachments
import newsbot.items.dated_item as dated_item
import string
import pape.utilities


class FrontierInvestigationFiling(
    emailable_item_with_attachments.EmailableItemWithAttachments,
    dated_item.DatedItem,
):
    filing_name_map = scrapy.Field()
    
    def synthesize_email_subject(self) -> str:
        filing_or_filings = pape.utilities.pluralize(
            singular_form = "new Frontier investigation filing",
            count = len(self["filing_name_map"]),
        )
        filing_or_filings = filing_or_filings[0].upper() + filing_or_filings[1:]
        
        return (
            f"{filing_or_filings} published "
            f"{self['datetime'].strftime('%A, %B %e')}"
        )
    
    def synthesize_html_email_body(self) -> str:
        filing_count = len(self["filing_name_map"])
        
        filing_or_filings = pape.utilities.pluralize(
            singular_form = "filing",
            count =         filing_count,
        ).capitalize()
        
        it_is_or_they_are = pape.utilities.pluralize(
            singular_form = "The filing is",
            plural_form =   "The filings are",
            count =         filing_count,
            include_count = False,
        )
        
        here_it_they_is_are = pape.utilities.pluralize(
            singular_form = "Here is the link to the filing",
            plural_form =   "Here are the links to the filings",
            count =         filing_count,
            include_count = False,
        )
        
        return self._get_email_template().safe_substitute({
            "email_subject":        self.synthesize_email_subject(),
            "filing_or_filings":    filing_or_filings,
            "it_is_or_they_are":    it_is_or_they_are,
            "here_it_they_is_are":  here_it_they_is_are,
            "filing_date":          self["datetime"].strftime("%A, %b. %e"),
            "filing_link_list":     self._synthesize_filing_link_list(),
        })
    
    def _synthesize_filing_link_list(self) -> str:
        all_items = "".join([
            f"""
                <li>
                    <a href="{each_link}">
                        {each_name}
                    </a>
                </li>
            """
            for each_name, each_link
            in self['filing_name_map'].items()
        ])
        
        return f"""
            <ul>
                {all_items}
            </ul>
        """
