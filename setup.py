# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import setuptools
import NewsBot.settings

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name        = NewsBot.settings.BOT_NAME,
    version     = NewsBot.settings._BOT_VERSION,
    
    author          = "Carter Pape",
    author_email    = "creator@newsbot.carterpape.com",
    
    packages    = setuptools.find_packages(),
    scripts     = [
        
    ],
    
    long_description                = long_description,
    long_description_content_type   = "text/markdown",
)
