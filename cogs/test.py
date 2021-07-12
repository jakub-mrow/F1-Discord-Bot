import discord
from discord import embeds
from discord.ext import commands
from discord import Embed
import requests
import json
import sys
from graphics.emojis import Emoji
from bs4 import BeautifulSoup

class Testing(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Events in cogs
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online from testing!")

    #Commands in cogs
    @commands.command(name = 'clear')
    async def clear(self, ctx, amount = 5):
        await ctx.channel.purge(limit = amount+1)

    @commands.command(name = "next-race")
    async def next_race(self,ctx):
        round_num = get_next_round()
        race_name = get_schedule(round_num)
        data, race_name = get_weekend_timings(race_name)

        next_race_embed = Embed(title = "Next race in Formula 1!", description = "{} \n Round: {}".format(race_name, round_num), colour = 0x19c3e1)
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
    client.add_cog(Testing(client))

def get_weekend_timings(race_name):
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