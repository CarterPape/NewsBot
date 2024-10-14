# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
from newsbot.db_connections import db_connection
from newsbot.items import maine_breach


class FilteredBreachesDBConnection(db_connection.DBConnection):
    @property
    def table_name(self):
        return "filtered_breaches"
    
    @property
    def table_definition(self):
        return f"""
            CREATE TABLE `{self.table_name}` (
                `breach_id`     INTEGER     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `organization`  TEXT,
                `people_affected` TEXT,
                `org_type`      TEXT,
                `reported_date` TEXT,
                `details_url`   TEXT        NOT NULL
            )
        """
    
    def record_breach_exclusion(self,
        breach: maine_breach.MaineBreach,
    ):
        db_cursor = self.cursor()
        db_cursor.execute(
            f"""
                INSERT INTO `{self.table_name}` (
                    organization,
                    org_type,
                    people_affected,
                    reported_date,
                    details_url
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """,
            (
                breach["organization_name"],
                breach["org_type"],
                breach["people_affected"],
                breach["reported_date"],
                breach["details_url"],
            )
        )
        self.commit()
        db_cursor.close()
    
    def is_breach_excluded(self,
        breach: maine_breach.MaineBreach,
    ) -> bool:
        db_cursor = self.cursor()
        db_cursor.execute(
            f"""
                SELECT
                    COUNT(*)
                FROM {self.table_name}
                WHERE
                    details_url = %s
            """,
            (
                breach["details_url"],
            )
        )
        
        match_count = typing.cast(list[int],
            db_cursor.fetchone(),
        )[0]
        db_cursor.close()
        return match_count > 0
