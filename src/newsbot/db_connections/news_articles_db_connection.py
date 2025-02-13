# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

from newsbot.db_connections import db_connection
from newsbot.db_connections import news_sources_db_connection
from newsbot.items import news_article
from newsbot.items import news_source


class NewsArticlesDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "news_articles"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `article_id`        INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `news_source_id`    TEXT        NOT NULL,
                `article_clean_url` TEXT        NOT NULL
            )
        """
    
    @property
    def connection_dependencies(self) -> list[type]:
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
                '{from_news_source.source_id}',
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
        
        the_row = db_cursor.fetchone()
        assert isinstance(the_row, tuple)
        
        match_count = the_row[0]
        assert isinstance(match_count, int)
        
        db_cursor.close()
        return match_count > 0
