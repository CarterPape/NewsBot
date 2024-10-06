# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=too-many-instance-attributes

class JavascriptQuoteParser:
    def __init__(self):
        self._master_string:        str
        self._completed_matches:    list[str]
        self._current_match:        str
        self._in_quotation:         bool
        self._in_entity:            bool
        self._keep_quotes:          bool
        
        self._current_index:        int
        self._current_character:    str
    
    def get_quotation_list(self, *,
        from_js_code:   str,
        keep_quotes:    bool =  False,
    ):
        self._master_string =       from_js_code
        self._completed_matches =   []
        self._current_match =       ""
        self._in_quotation =        False
        self._in_entity =           False
        self._keep_quotes =         keep_quotes
        
        for self._current_index in range(len(self._master_string)):
            self._current_character = self._master_string[self._current_index]
            
            if (
                self._current_character == '\\'
            ) and (
                self._in_entity is False
            ):
                self._handle_entity_start()
            
            elif (self._in_entity is True):
                self._resolve_current_entity()
            
            elif (
                self._current_character_is_quote()
            ) and (
                self._in_quotation is False
            ):
                self._handle_new_quotation()
            
            elif (
                self._current_character_is_quote()
            ) and (
                self._in_quotation is True
            ):
                self._resolve_current_quotation()
            
            elif (self._in_quotation is True):
                self._current_match += self._current_character
        
        return self._completed_matches
    
    def _current_character_is_quote(self):
        return self._current_character in ['"', "'"]
    
    def _handle_entity_start(self):
        self._in_entity = True
        if (self._in_quotation is True):
            self._current_match += self._current_character
    
    def _resolve_current_entity(self):
        self._in_entity = False
        if (self._in_quotation is True):
            self._current_match += self._current_character
    
    def _handle_new_quotation(self):
        self._in_quotation = True
        if self._keep_quotes:
            self._current_match += self._current_character
    
    def _resolve_current_quotation(self):
        if self._keep_quotes:
            self._current_match += self._current_character
        
        self._completed_matches.append(self._current_match)
        self._current_match = ""
        self._in_quotation = False
