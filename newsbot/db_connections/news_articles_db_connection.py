# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import scrapy.settings
import newsbot.db_connections.db_connection as db_connection
import newsbot.db_connections.news_sources_db_connection as news_sources_db_connection
import newsbot.items.news_article as news_article
import newsbot.items.news_source as news_source
import datetime


class NewsArticlesDBConnection(db_connection.DBConnection):
    def __init__(self,
        *args,
        settings: scrapy.settings.Settings,
        **kwargs,
    ):
        super().__init__(
            *args,
            settings =  settings,
            **kwargs,
        )
        
        self._news_sources_table = news_sources_db_connection.NewsSourcesDBConnection(
            settings = settings,
        )
    
    @property
    def table_name(self):
        return "news_articles"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `article_id`        INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `news_source_id`    INTEGER,
                `article_clean_url` TEXT        NOT NULL,
                FOREIGN KEY (news_source_id)
                    REFERENCES {self._news_sources_table.table_name}(source_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
        """
    
    @property
    def connection_dependencies(self) -> typing.List[type]:
        return [news_sources_db_connection.NewsSourcesDBConnection]
    
    def record_news_article(self,
        article: news_article.NewsArticle,
        *,
        from_news_source: news_source.NewsSource,
    ):
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            INSERT INTO `{self.table_name}` (
                news_source_id,
                article_clean_url
            )
            VALUES (
                {from_news_source.source_id},
                '{article.clean_url}'
            )
        """)
        self.commit()
        db_cursor.close()
    
    def news_article_seen(self,
        article: news_article.NewsArticle
    ) -> bool:
        db_cursor = self.cursor()
        db_cursor.execute(f"""
            SELECT
                COUNT(*)
            FROM {self.table_name}
            WHERE
                article_clean_url = {article.clean_url}
        """)
        
        match_count = db_cursor.fetchone()[0]
        db_cursor.close()
        return match_count > 0
