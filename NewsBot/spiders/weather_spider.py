# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

url = "https://developers.synopticdata.com/mesonet/explorer/"
datetime_request_format = "%Y%m%d%H%M"

precipitation_endpoint = "https://api.synopticdata.com/v2/stations/precipitation"
precipitation_request_data = {
    "token":    "1eb998f36302484fa1f4abb111bab1f9",
    "stid":     "MOAB",
    "start":    "201910010000", # except the API takes UTC times, so this needs to be converted from local to UTC
    "end":      "202009302359", # as does this
    "units":    "precip|in",
}


history_endpoint = "https://api.synopticdata.com/v2/stations/timeseries?&token=1eb998f36302484fa1f4abb111bab1f9&stid=MOAB&start=202002150000&end=202002230000&units=temp|f&obtimezone=local&timeformat=%F %T%z"
history_request_data = {
    "token":    "1eb998f36302484fa1f4abb111bab1f9",
    "stid":     "MOAB",
    "start":    "202002150000", # and this
    "end":      "202002230000", # and this
    "units":    "temp|f",
    "obtimezone":   "local",
    "timeformat":   "%F %T%z",
}

forecast_endpoint = "https://forecast.weather.gov/MapClick.php?lat=38.5733&lon=-109.5508&unit=0&lg=english&FcstType=dwml"
