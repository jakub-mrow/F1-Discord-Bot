import requests
import json
import pprint

response = requests.get("http://ergast.com/api/f1/current.json")

my_json = response.text
parsed = json.loads(my_json)
#print(json.dumps(parsed, indent=4, sort_keys=True))


def get_schedule():
    response = requests.get("http://ergast.com/api/f1/current.json")
    my_json = response.text
    parsed = json.loads(my_json)
    data = {}
    
    for item in parsed["MRData"]["RaceTable"]["Races"]:
        country = item["Circuit"]["Location"]["country"]
        race_name = item["raceName"]
        race_date = item["date"]
        race_time = item["time"]
        data[item["round"]] = [country, race_name, race_date, race_time]
    return data

d = get_schedule()
print(d)





