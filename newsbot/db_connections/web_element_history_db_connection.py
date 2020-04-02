# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.settings
import datetime
import pytz
import typing
import difflib
import newsbot.db_connections.db_connection as db_connection
import newsbot.items.emailable_item as emailable_item
import newsbot.items.web_element as web_element


class WebElementHistoryDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "web_element_history"
    
    def __init__(self, *args, settings: scrapy.settings.Settings, **kwargs):
        super().__init__(
            self,
            *args,
            settings = settings,
            **kwargs
        )
        self._current_web_element: web_element.WebElement
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `web_element_instance`  INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `url`                   TEXT        NOT NULL,
                `instance_content`      MEDIUMTEXT  NOT NULL,
                `first_appearance`      DATETIME    NOT NULL,
                `latest_appearance`     DATETIME    NOT NULL,
                `instance_is_current`   BOOLEAN     NOT NULL
            )
        """
    
    def record_web_element(self,
        item_to_record: web_element.WebElement
    ):
        raise NotImplementedError
    
    def current_web_element_is_new(self) -> bool:
        raise NotImplementedError
