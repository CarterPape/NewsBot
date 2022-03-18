# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import dotenv
import os
import urllib.parse
import requests
import datetime
import pytz
import pape.utilities

dotenv.load_dotenv(dotenv.find_dotenv())


synoptic_request_time_format = "%Y%m%d%H%M"
synoptic_response_time_format = "%Y-%m-%dT%H:%M:%S%z"

def most_recent_wednesday_midnight():
    mountain_timezone = pytz.timezone("US/Mountain")
    now = datetime.datetime.now()
    wednesday_index = 2
    days_offset = (now.weekday() - wednesday_index) % 7
    time_offset = datetime.datetime.combine(datetime.date.min, now.time()) - datetime.datetime.min
    latest_wednesday = (now - datetime.timedelta(days = days_offset)) - time_offset
    return mountain_timezone.localize(latest_wednesday)

def seven_days_ago(the_datetime):
    naïve_datetime = the_datetime.replace(tzinfo = None)
    return pytz.timezone("US/Mountain").localize(naïve_datetime - datetime.timedelta(days = 7))


end_time_locally = most_recent_wednesday_midnight()
end_time_as_utc = end_time_locally.astimezone(pytz.utc)
end_time_string = end_time_as_utc.strftime(synoptic_request_time_format)
start_time_locally = seven_days_ago(end_time_locally)
start_time_as_utc = start_time_locally.astimezone(pytz.utc)
start_time_string = start_time_as_utc.strftime(synoptic_request_time_format)


daily_relevant_data_init: dict[str: str] = {
    "high": None,
    "low": None,
    "precipitation": None,
}
relevant_history_data: dict[str: dict] = {}


# precipitation_endpoint = "https://api.synopticdata.com/v2/stations/precip"
# precipitation_request_data = {
#     "token":        os.getenv("SYNOPTIC_DATA_TOKEN"),
#     "stid":         "MOAB",
#     "start":        start_time_string,
#     "end":          end_time_string,
#     "units":        "precip|in",
#     "pmode":        "intervals",
#     "interval":     "day",
#     "obtimezone":   "local",
#     "timeformat":   synoptic_response_time_format,
# }
# precipitation_request_url = (
#     precipitation_endpoint
#     + "?"
#     + urllib.parse.urlencode(precipitation_request_data)
# )

# precipitation_data_response = requests.get(precipitation_request_url)
# precipitation_data = precipitation_data_response.json()


# for each_datapoint in precipitation_data["STATION"][0]["OBSERVATIONS"]["precipitation"]:
#     each_date = datetime.datetime.strptime(
#         each_datapoint["first_report"],
#         synoptic_response_time_format
#     )
#     each_date_string = pape.utilities.ap_style_date_string(each_date, use_period = False)
    
#     formatted_relevant_history_data[each_date_string] = daily_relevant_formatted_data_init.copy()
#     each_total = each_datapoint["total"]
#     each_total_string = (
#         str(each_total).lstrip("0") if each_total != 0
#         else "---"
#     )
#     formatted_relevant_history_data[each_date_string]["precipitation"] = each_total_string


history_endpoint = "https://api.synopticdata.com/v2/stations/timeseries"
history_request_data = {
    "token":        os.getenv("SYNOPTIC_DATA_TOKEN"),
    "stid":         "MOAB",
    "start":        start_time_string,
    "end":          end_time_string,
    "units":        "english",
    "precip":       1,
    "obtimezone":   "local",
    "timeformat":   synoptic_response_time_format,
}
history_request_url = (
    history_endpoint
    + "?"
    + urllib.parse.urlencode(history_request_data)
)

history_data_response = requests.get(history_request_url)
history_data = history_data_response.json()


historic_observations = history_data["STATION"][0]["OBSERVATIONS"]

previous_precipitation_accumulation = 0

for each_observation_index in range(len(historic_observations["date_time"]) - 1):
    each_datetime = datetime.datetime.strptime(
        historic_observations["date_time"][each_observation_index],
        synoptic_response_time_format,
    )
    each_date_string = pape.utilities.ap_style_date_string(each_datetime.date(), use_period = False)
    
    each_temperature = historic_observations["air_temp_set_1"][each_observation_index]
    
    if each_date_string in relevant_history_data:
        relevant_history_data[each_date_string]["high"] = max(
            each_temperature,
            relevant_history_data[each_date_string]["high"]
        )
        relevant_history_data[each_date_string]["low"] = min(
            each_temperature,
            relevant_history_data[each_date_string]["low"]
        )
    else:
        relevant_history_data[each_date_string] = daily_relevant_data_init.copy()
        relevant_history_data[each_date_string]["high"] = each_temperature
        relevant_history_data[each_date_string]["low"] = each_temperature
    
    if each_datetime.hour == 23:
        relevant_history_data[each_date_string]["precipitation"] = (
            historic_observations["precip_accumulated_set_1d"][each_observation_index + 1]
            - previous_precipitation_accumulation
        )
        previous_precipitation_accumulation += (
            relevant_history_data[each_date_string]["precipitation"]
        )


for each_formatted_date, each_observation_set in relevant_history_data.items():
    each_precipitation_observation = each_observation_set["precipitation"]
    each_precipitation_string = (
        f"{each_precipitation_observation or 0:.2f}".lstrip("0") if each_precipitation_observation != 0
        else "---"
    )
    print(
        f"{each_formatted_date}"
        + f"\t{each_observation_set['high']:.0f}"
        + f"\t{each_observation_set['low']:.0f}"
        + f"\t{each_precipitation_string}"
    )


forecast_endpoint = "https://forecast.weather.gov/MapClick.php"
forecast_request_data = {
    "lat":      "38.5733",
    "lon":      "-109.5508",
    "unit":     "0",
    "lg":       "english",
    "FcstType": "dwml",
}
forecast_request_url = (
    forecast_endpoint
    + "?"
    + urllib.parse.urlencode(forecast_request_data)
)
