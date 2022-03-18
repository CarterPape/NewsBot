# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import json
import abc

import scrapy


class SelfSerializingItem(
    scrapy.Item,
    metaclass = abc.ABCMeta,
):
    def serialized(self) -> str:
        simple_self = {}
        
        for field_key, field_properties in self.fields.items():
            if (
                "ignore_when_serializing" in field_properties
            ) and (
                field_properties["ignore_when_serializing"]
            ):
                continue
            
            else:
                if "serializer" in field_properties:
                    simple_self[field_key] = field_properties["serializer"](self[field_key])
                elif issubclass(type(self[field_key]), SelfSerializingItem):
                    simple_self[field_key] = self[field_key].serialized()
                elif (
                    issubclass(type(self[field_key]), list)
                ):
                    simple_self[field_key] = [
                        each_item.serialized()
                        if issubclass(type(each_item), SelfSerializingItem)
                        else each_item
                        for each_item in self[field_key]
                    ]
                else:
                    simple_self[field_key] = self[field_key]
        
        return json.dumps(simple_self, sort_keys = True)
