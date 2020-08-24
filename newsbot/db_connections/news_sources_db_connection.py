# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import newsbot.db_connections.db_connection as db_connection
import newsbot.db_connections.news_sources_db_connection as news_sources_db_connection
import newsbot.items.news_article as news_article
import newsbot.items.news_source as news_source
import datetime
import newsbot.exceptions.duplicate_entry_exception as duplicate_entry_exception


class NewsSourcesDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "news_sources"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `source_id`         INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `source_name`       TEXT        NOT NULL,
                `source_url`        TEXT        NOT NULL,
                `links_xpath`       TEXT        NOT NULL,
            )
        """
    
    def add_source(self,
        source: news_source.NewsSource,
        *,
        same_name_is_duplicate =    True,
        same_url_is_duplicate =     True,
    ):
        if same_name_is_duplicate or same_url_is_duplicate:
            self._raise_if_existing(
                source_to_look_for =        source,
                same_name_is_duplicate =    same_name_is_duplicate,
                same_url_is_duplicate =     same_url_is_duplicate,
            )
        
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            INSERT INTO `{self.table_name}` (
                source_name,
                source_url,
                links_xpath
            )
            VALUES (
                '{source.name}',
                '{source.url}',
                '{source.links_xpath}'
            )
        """)
        self.commit()
        db_cursor.close()
    
    def _raise_if_existing(self,
        *,
        source_to_look_for:     news_source.NewsSource,
        same_name_is_duplicate: bool,
        same_url_is_duplicate:  bool,
    ):
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT
                COUNT(*)
            FROM {self.table_name}
            WHERE (
                {same_name_is_duplicate} AND source_name = {source_to_look_for.name}
            ) OR (
                {same_url_is_duplicate} AND source_url = {source_to_look_for.url}
            )
        """)
        
        match_count = db_cursor.fetchone()[0]
        db_cursor.close()
        
        if match_count > 0:
            raise duplicate_entry_exception.DuplicateEntryException()
    
    def list_all_sources(self) -> [news_source.NewsSource]:
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT
                source_id,
                source_name,
                source_url,
                links_xpath
            FROM {self.table_name}
        """)
        
        source_tuple_list = db_cursor.fetchall()
        db_cursor.close()
        
        return [
            news_source.NewsSource(
                source_id =     each_tuple[0],
                source_name =   each_tuple[1],
                source_url =    each_tuple[2],
                links_xpath =   each_tuple[3],
            )
            for each_tuple
            in source_tuple_list
        ]
