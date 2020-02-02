# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import setuptools
import NewsBot.settings

setuptools.setup(
    name        = NewsBot.settings.BOT_NAME,
    version     = NewsBot.settings._BOT_VERSION,
    packages    = setuptools.find_packages(),
)
