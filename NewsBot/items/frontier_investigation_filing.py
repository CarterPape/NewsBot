# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import NewsBot.items.emailable_item
import NewsBot.items.dated_item
import NewsBot.items.item_with_files
import string
import pape.utilities


class FrontierInvestigationFiling(
    NewsBot.items.emailable_item.EmailableItem,
    NewsBot.items.dated_item.DatedItem,
    NewsBot.items.item_with_files.ItemWithFiles,
):
    filing_name_map = scrapy.Field()
    
    @property
    def email_subject(self) -> str:
        filing_or_filings = pape.utilities.pluralize(
            singular_form = "new Frontier investigation filing",
            count = len(self["filing_name_map"]),
        )
        filing_or_filings = filing_or_filings[0].upper() + filing_or_filings[1:]
        
        return (
            f"{self._filing_or_filings} filed "
            f"{self['datetime'].strftime('%A, %b. %e')}"
        )
    
    @property
    def html_email_body(self) -> str:
        filing_count = len(self["filing_name_map"])
        
        filing_or_filings = pape.utilities.pluralize(
            singular_form = "filing",
            count =         filing_count,
        ).capitalize()
        
        it_is_or_they_are = pape.utilities.pluralize(
            singular_form = "It is",
            plural_form =   "They are",
            count =         filing_count,
            include_count = False,
        )
        
        here_it_they_is_are = pape.utilities.pluralize(
            singular_form = "Here is the link to the filing",
            plural_form =   "Here are the links to the filings",
            count =         filing_count,
            include_count = False,
        )
        
        return self._email_template.safe_substitute({
            "email_subject":        self.email_subject,
            "filing_or_filings":    filing_or_filings,
            "it_is_or_they_are":    it_is_or_they_are,
            "here_it_they_is_are":  here_it_they_is_are,
            "filing_date":          self["datetime"].strftime("%A, %b. %e"),
            "filing_link_list":     self._filing_link_list,
        })
    
    @property
    def _filing_link_list(self) -> str:
        all_items = [
            f"""
                <li>
                    <a href="{each_link}">
                        {each_name}
                    </a>
                </li>
            """
            for each_name, each_link
            in self['filing_name_map'].items()
        ]
        
        return f"""
            <ul>
                {all_items}
            </ul>
        """
