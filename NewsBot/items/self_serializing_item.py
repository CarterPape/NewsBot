# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import json


class SelfSerializingItem(scrapy.Item):
    def serialized(self, *,
        skip_keys: bool = True,
    ) -> dict:
        
        simple_self = dict()
        
        for field_key in self.fields:
            field_properties = self.fields[field_key]
            
            if (
                hasattr(field_properties, "ignore_when_serializing")
            ) and (
                field_properties["ignore_when_serializing"]
            ):
                continue
            
            else:
                try:
                    if hasattr(field_properties, "serializer"):
                        simple_self[field_key] = field_properties["serializer"](self[field_key])
                    else:
                        simple_self[field_key] = self[field_key]
                
                except KeyError:
                    if skip_keys:
                        continue
                    else:
                        raise
        
        return simple_self
