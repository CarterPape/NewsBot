# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import json


class SelfSerializingItem(scrapy.Item):
    _serialized = scrapy.Field(ignore_when_serializing = True)
    
    def serialized(self) -> dict:
        if "_serialized" in self:
            pass
        else:
            simple_self = dict()
            
            for field_key, field_properties in self.fields.items():
                if (
                    "ignore_when_serializing" in field_properties
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
                        continue
            
            self["_serialized"] = json.dumps(simple_self, sort_keys = True)
        
        return self["_serialized"]
