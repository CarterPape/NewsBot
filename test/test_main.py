# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

# For each parser test file, I am going to maintain a cache and snapshot test. I should be able to use parameterization and marks to elegantly determine which type of test to run --- or both.
# Caching should be handled by scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware. It's probably fine to cache a file for just a day, but I do need to figure out how to avoid requesting a bunch of pages simultaneously.
# Snapshot tests should use a fixture that reads from a file in the test directory. Snapshot files should be updated only manually.
