# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import os.path
import glob
import pape.utilities

_submodules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

for each_file in _submodules:
    if os.path.isfile(each_file) and (os.path.basename(each_file) != '__init__.py'):
        each_module = __import__(
            name = 
                f"{__name__}."
                f"""{
                    pape.utilities.strip_file_extension(
                        from_path = each_file,
                        basename_only = True,
                    )
                }""",
            fromlist = ["*"],
        )
        for symbol in dir(each_module):
            if symbol not in locals():
                locals()[symbol] = getattr(each_module, symbol)
