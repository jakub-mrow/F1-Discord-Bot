import discord
from discord.ext import commands
from discord import Embed
import requests
import json
from graphics.emojis import Emoji
from bs4 import BeautifulSoup

class RaceInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "schedule")
    async def schedule(self, ctx):
        data = get_schedule()
        schedule_embed = Embed(title = "2021 Race Schedule", description = ':date: :date: :date:', colour = 0x19c3e1)
        fields = []
        for key, value in data.items():
            race_name = data[key][1]
            country = data[key][0]
            race_date = data[key][2]
            race_time = data[key][3]
            fields.append(("Round {}: {}".format(key, race_name),"Date: {} Country: {}".format(race_date, country),False))

        for name, value, inline in fields:
            schedule_embed.add_field(name = name, value = value, inline = inline)

        await ctx.send(embed = schedule_embed)

    @commands.command(name = "last-race")
    async def last_race(self,ctx):
        grid_result, add_info = get_last_race()
        last_race_embed = Embed(title = "{}!".format(add_info[1]), description = "Round: {} - {}".format(add_info[0], add_info[2]), colour = 0x19c3e1)

        em = Emoji()
        emoji_list = em.data

        # Top 3 places in Embed 
        last_race_embed.add_field(name = "{} {} | {}".format(":first_place:", grid_result[0], emoji_list[grid_result[0]]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {} | {}".format(":second_place:", grid_result[1], emoji_list[grid_result[1]]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {} | {}".format(":third_place:", grid_result[2], emoji_list[grid_result[2]]), value = '\u200b', inline = True)

        # Rest of the drivers
        for i in range(1, len(grid_result)+1):
            if i > 3:
                last_race_embed.add_field(name = "{}. {} | {}".format(i,grid_result[i-1], emoji_list[grid_result[i-1]]), value = '\u200b', inline = False)

        await ctx.send(embed = last_race_embed)


    @commands.command(name = "next-race")
    async def next_race(self,ctx):
        round_num = get_next_round()
        race_name = get_schedule_next(round_num)
        data, race_name_ret = get_weekend_timings(race_name)

        next_race_embed = Embed(title = "Next race in Formula 1!", description = "{} \n Round: {}".format(race_name_ret, round_num), colour = 0x19c3e1)
        fields = []
        for racing in data:
            start_date = data[racing]["start"][0]
            start_time = data[racing]["start"][1]
            end = data[racing]["end"][1]
            offset = data[racing]["offset"]

            start_time = convert_time(start_time, offset)
            end = convert_time(end, offset)

            times = "Start: {} \n End: {}".format(start_time,end)
            race_type = "{} {}".format(racing.title(), start_date)
            fields.append((race_type, times, False)) 

        for text, value, inline in fields:
            next_race_embed.add_field(name = text, value = value, inline = inline)
        await ctx.send(embed = next_race_embed)

def setup(client):
    client.add_cog(RaceInfo(client))

# returns schedule of current year
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

# returns last race finish places plus additional informacion about race 
def get_last_race():
    response = requests.get("http://ergast.com/api/f1/current/last/results.json")
    my_json = response.text
    parsed = json.loads(my_json)
    grid = []
    race_info = []

    for item in parsed["MRData"]["RaceTable"]["Races"][0]["Results"]:
        grid.append(item["Driver"]["code"])

    date = parsed["MRData"]["RaceTable"]["Races"][0]["date"]
    race_round = parsed["MRData"]["RaceTable"]["Races"][0]["round"]
    race_name = parsed["MRData"]["RaceTable"]["Races"][0]["raceName"]
    race_info.append(race_round)
    race_info.append(race_name)
    race_info.append(date)
    
    return grid, race_info

# web scraping times of race, quali, practices from f1 site 
def get_weekend_timings(race_name):
    URL = "https://www.formula1.com/en/racing/2021/"+race_name+".html"
    #URL = "https://www.formula1.com/en/racing/2021/Great_Britain.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    weekend_rounds = ["row js-race", "row js-qualifying","row js-practice-3","row js-practice-2", "row js-practice-1"]
    new_format_races = ["Great_Britain"] # tab of races with new format
    new_format = ["row js-race", "row js-sprint", "row js-practice-2", "row js-qualifying", "js-practice-1"] 
    data = {}

    if race_name in new_format_races:
        for racing in new_format:
            splitted = racing.split("-")[1:]
            joined = "-".join(splitted)
            
            info_time = soup.find("div", class_= racing)
            start = info_time["data-start-time"].split("T")
            end = info_time["data-end-time"].split("T")
            offset = info_time["data-gmt-offset"]

            if joined not in data:
                data[joined] = {"start": start, "end": end, "offset": offset}
    else:
        for racing in weekend_rounds:
            splitted = racing.split("-")[1:]
            joined = "-".join(splitted)

            info_time = soup.find("div", class_= racing)
            start = info_time["data-start-time"].split("T")
            end = info_time["data-end-time"].split("T")
            offset = info_time["data-gmt-offset"]

            if joined not in data:
                data[joined] = {"start": start, "end": end, "offset": offset}

    race_name_ret = soup.find("h2", class_="f1--s").string

    return data, race_name_ret

# returns round number for next round 
def get_next_round():
    response = requests.get("http://ergast.com/api/f1/current/last/results.json")
    my_json = response.text
    parsed = json.loads(my_json)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    round_num = int(parsed["MRData"]["RaceTable"]["Races"][0]["round"]) + 1

    return round_num

# this method returns name of the country for webscraping f1 site
def get_schedule_next(round_num):
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

# time converting for european time zone 
def convert_time(time, offset):
    time_num = int(time.split(":")[0])
    offset = int(offset.split(":")[0])
    if offset < 2:
        time_num = time_num + 2 - offset
    if offset > 2:
        time_num = time_num - (offset - 2)
    time = "{}:{}".format(time_num, time.split(":")[1])
    return time