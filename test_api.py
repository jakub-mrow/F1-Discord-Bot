import requests
import json
import pprint
from bs4 import BeautifulSoup

def get_weekend_timings(race_name):
    race_name = "Hungary"
    URL = "https://www.formula1.com/en/racing/2021/"+race_name+".html"
    #URL = "https://www.formula1.com/en/racing/2021/Great_Britain.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    weekend_rounds = ["row js-race", "row js-qualifying","row js-practice-3","row js-practice-2", "row js-practice-1"]
    data = {}

    for racing in weekend_rounds:
        splitted = racing.split("-")[1:]
        joined = "-".join(splitted)

        info_time = soup.find("div", class_= racing)
        start = info_time["data-start-time"].split("T")
        end = info_time["data-end-time"].split("T")
        offset = info_time["data-gmt-offset"]

        if joined not in data:
            data[joined] = {"start": start, "end": end, "offset": offset}

    race_name = soup.find("h2", class_="f1--s").string

    return data, race_name
    
def get_next_round():
    response = requests.get("http://ergast.com/api/f1/current/last/results.json")
    my_json = response.text
    parsed = json.loads(my_json)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    round_num = int(parsed["MRData"]["RaceTable"]["Races"][0]["round"]) + 1

    return round_num

def get_schedule(round_num):
    round_num = round_num - 1
    response = requests.get("http://ergast.com/api/f1/current.json")
    my_json = response.text
    parsed = json.loads(my_json)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    country_name = parsed["MRData"]["RaceTable"]["Races"][round_num]["Circuit"]["Location"]["country"]

    if country_name == "UK":
        country_name = "Great_Britain"
    if country_name == "UAE":
        country_name = "United_Arab_Emirates"
    if country_name == "USA":
        country_name = "United_States"

    return country_name

def convert_time(time, offset):
    time_num = int(time.split(":")[0])
    offset = int(offset.split(":")[0])
    if offset < 2:
        time_num = time_num + 2 - offset
    if offset > 2:
        time_num = time_num - (offset - 2)
    time = "{}:00".format(time_num)
    return time
    
round_num = get_next_round()
race_name = get_schedule(round_num)

data, race_name_ret = get_weekend_timings(race_name)
fields = []

for racing in data:
    start_date = data[racing]["start"][0]
    start_time = data[racing]["start"][1]
    end = data[racing]["end"][1]
    
    times = "Start: {} End: {}".format(start_time,end)

    race_type = "{} {}".format(racing.title(), start_date)

    fields.append((race_type, times, False))


def get_last_round():
    response = requests.get("http://ergast.com/api/f1/current/last/results.json")
    my_json = response.text
    parsed = json.loads(my_json)
    round_num = int(parsed["MRData"]["RaceTable"]["Races"][0]["round"])
    return round_num


def get_quali_times(round):
    response = requests.get("http://ergast.com/api/f1/2021/{}/qualifying.json".format(round))
    my_json = response.text
    parsed = json.loads(my_json)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    data = {}
    for item in parsed["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]:
        driver_name = item["Driver"]["code"]
        data[driver_name] = []
        if "Q1" in item:
            data[driver_name].append(item["Q1"])
        if "Q2" in item:
            data[driver_name].append(item["Q2"])
        if "Q3" in item:
            data[driver_name].append(item["Q3"])
        else:
            if len(data[driver_name]) == 1:
                for _ in range(2):
                    data[driver_name].append("--")
            else:
                data[driver_name].append("--")
    return data
round_num = get_last_round()
quali = get_quali_times(round_num)
#print(quali)
for driver in quali:
    quali_1 = quali[driver][0]
    quali_2 = quali[driver][1]
    quali_3 = quali[driver][2]
    times = "Q1: {} Q2: {} Q3: {}".format(quali_1, quali_2, quali_3)
    #print(times)

# returns name of Grand Prix
def get_gp_name(round_num):
    response = requests.get("http://ergast.com/api/f1/current.json")
    my_json = response.text
    parsed = json.loads(my_json)
    gp_name = parsed["MRData"]["RaceTable"]["Races"][round_num]["raceName"]
    return gp_name

get_gp_name(10)