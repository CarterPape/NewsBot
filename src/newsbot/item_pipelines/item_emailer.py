# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import logging
import types

import scrapy.spiders
import scrapy.settings
import scrapy.mail
import scrapy.utils.defer
import scrapy.exceptions
import twisted.internet.defer
import twisted.python.failure

from newsbot.db_connections import email_subscriptions_db_connection
from newsbot.items import emailable_item
from newsbot.items import emailable_item_with_attachments
from newsbot.item_pipelines import item_pipeline


class ItemEmailer(item_pipeline.ItemPipeline):
    def __init__(self):
        self._settings: scrapy.settings.Settings
    
    def process_item(self,
        item:   emailable_item.EmailableItem,
        spider: scrapy.spiders.Spider,
    ) -> scrapy.Item | twisted.internet.defer.Deferred:
        try:
            logging.debug(f"Processing item {item} from spider {spider}")
        except RecursionError:
            logging.debug(f"Processing item {item} from a spider with a shitty repl implementation")
        
        self._settings = spider.settings
        
        item["email_sent_datetime"] = datetime.datetime.now()
        possible_deferred = self._try_to_email_item(item)
        
        if possible_deferred is None:
            return item
        else:
            possible_deferred.addCallback(self._email_sent, item)
            possible_deferred.addErrback(self._email_failed, item)
            return possible_deferred
    
    def _try_to_email_item(self,
        item: emailable_item.EmailableItem,
    ) -> twisted.internet.defer.Deferred | None:
        if isinstance(
            item,
            emailable_item_with_attachments.EmailableItemWithAttachments,
        ):
            
            attachments = item.gather_email_attachments()
        else:
            attachments = None
        
        db_connection = (
            email_subscriptions_db_connection.EmailSubscriptionsDBConnection(
                settings = self._settings
            )
        )
        
        addressee_list = db_connection.get_addressees_that_should_receive(item)
        formatted_addressee_list = [
            (
                f"{addressee[0]} <{addressee[1]}>"
                if addressee[0] is not None
                else f"{addressee[1]}"
            )
            for addressee
            in addressee_list
        ]
        
        emailer = scrapy.mail.MailSender.from_settings(self._settings)
        emailer.debug = self._settings.getbool("_PRINT_INSTEAD_OF_EMAIL")
        
        return emailer.send(
            to = formatted_addressee_list,
            subject = item.synthesize_email_subject(),
            body = item.synthesize_html_email_body(),
            mimetype = "text/html",
            charset = "utf-8",
            attachs = attachments,
        )
    
    def _email_sent(self,
        _: types.NoneType,
        item: emailable_item.EmailableItem,
    ) -> scrapy.Item:
        logging.debug(f"Email sent for item {item}")
        return item
    
    def _email_failed(self,
        failure: twisted.python.failure.Failure,
        item: emailable_item.EmailableItem,
    ) -> twisted.python.failure.Failure:
        logging.error(f"Email failed for item {item}.\nThe failure was:\n{failure}")
        raise scrapy.exceptions.DropItem(f"Email failed for item {item} with failure {failure}")
