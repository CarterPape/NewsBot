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

import newsbot.concrete_subclass_loader
import newsbot.items.emailable_item
import pape.utilities
import newsbot.db_connections.email_subscriptions_db_connection as email_subscriptions_db_connection
import dotenv
import scrapy.utils.project

dotenv.load_dotenv(dotenv.find_dotenv())

os.environ["SCRAPY_SETTINGS_MODULE"] = "newsbot.settings"
project_settings = scrapy.utils.project.get_project_settings()

db_connection = email_subscriptions_db_connection.EmailSubscriptionsDBConnection(
    settings = project_settings
)

add_addressee = "yes"

print("Here are the current subscriptions:")
subscription_list = db_connection.get_all_subscriptions()
for subscription in subscription_list:
    print(
        (
            f"{subscription[0]} <{subscription[1]}>"
            if subscription[0] != None
            else f"{subscription[1]}"
        ) + (
            f"\n    subscribed to {subscription[2]}"
        )
    )
print()

print("Here are the items currently known to NewsBot:")
emailable_item_class_loader = newsbot.concrete_subclass_loader.ConcreteSubclassLoader(
    load_subclasses_of =    newsbot.items.emailable_item.EmailableItem,
    from_modules_named =    project_settings.getlist("_TOP_LEVEL_MODULES"),
)
for emailable_item_class in emailable_item_class_loader.list():
    print(pape.utilities.full_name(of_type = emailable_item_class))
print()

while (
    add_addressee.casefold() == "yes".casefold()
    or add_addressee.casefold() == "y".casefold()
):
    item_selection = input(
        "Enter item selection, using % as a wildcard: "
    ).strip()
    
    new_email_address = input(
        "Enter an email address to which to send the items: "
    ).strip()
    
    new_addressee_name = input(
        "Enter the name of the recipient, or leave blank if there is none: "
    ).strip()
    
    db_connection.add_subscription(
        addressee_name = new_addressee_name,
        email_address = new_email_address,
        item_selection = item_selection,
    )
    
    add_addressee = input(
        "The subscription was added. Would you like to add another? (y/n) "
    )
