# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

url = "https://developers.synopticdata.com/mesonet/explorer/"
datetime_request_format = "%Y%m%d%H%M"

precipitation_endpoint = "https://api.synopticdata.com/v2/stations/precip"
precipitation_request_data = {
    "token":    os.getenv("_SYNOPTIC_DATA_TOKEN"),
    "stid":     "MOAB",
    "start":    "202102100659", # except the API takes UTC times, so this needs to be converted from local to UTC
    "end":          "202102170659", # as does this
    "units":        "precip|in",
    "pmode":        "intervals",
    "interval":     "day",
    "obtimezone":   "local",
    "timeformat":   "%FT%T%z",
}


history_endpoint = "https://api.synopticdata.com/v2/stations/timeseries?&token=1eb998f36302484fa1f4abb111bab1f9&stid=MOAB&start=202002150000&end=202002230000&units=temp|f&obtimezone=local&timeformat=%FT%T%z"
history_request_data = {
    "token":    os.getenv("_SYNOPTIC_DATA_TOKEN"),
    "stid":     "MOAB",
    "start":    "202002150000", # and this
    "end":      "202002230000", # and this
    "units":    "temp|f",
    "obtimezone":   "local",
    "timeformat":   "%FT%T%z",
}

forecast_endpoint = "https://forecast.weather.gov/MapClick.php?lat=38.5733&lon=-109.5508&unit=0&lg=english&FcstType=dwml"
