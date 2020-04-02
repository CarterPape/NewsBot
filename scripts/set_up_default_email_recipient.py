#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import sys
import os
sys.path.append(os.getcwd())

import newsbot.db_connections.email_subscriptions_db_connection as email_subscriptions_db_connection
import dotenv
import scrapy.utils.project

dotenv.load_dotenv(dotenv.find_dotenv())

os.environ["SCRAPY_SETTINGS_MODULE"] = "newsbot.settings"
project_settings = scrapy.utils.project.get_project_settings()

db_connection = email_subscriptions_db_connection.EmailSubscriptionsDBConnection(
    settings = project_settings
)

if db_connection.table_exists():
    pass
else:
    db_connection.create_table()

db_cursor = db_connection.cursor()
db_cursor.execute("""
    SELECT
        addressee_name,
        email_address
    FROM email_subscriptions
    WHERE item_selection = '%'
""")
recipient_list = db_cursor.fetchall()
db_cursor.close()

if len(recipient_list) > 0:
    print("Looks like the following are already subscribed to all item emails:")
    for recipient in recipient_list:
        print(
            f"{recipient[0]} <{recipient[1]}>"
            if recipient[0] != None
            else f"{recipient[1]}"
        )
    add_catchall_addressee = False
else:
    add_catchall_addressee = True

if add_catchall_addressee:
    new_email_address = input(
        "Enter an email address that will receive all item emails: "
    ).strip()
    
    new_addressee_name = input(
        "Enter the name of the recipient, or leave blank if there is none: "
    ).strip()
    
    db_connection.add_subscription(
        addressee_name = new_addressee_name,
        email_address = new_email_address,
        item_selection = "%",
    )
    
    print("default subscription added")

print("To add further subscriptions, invoke ./scripts/add_email_subscription.py")
