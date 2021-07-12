import discord
from discord.ext import commands
from discord import Embed
import requests
import json
from graphics.emojis import Emoji

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
        last_race_embed.add_field(name = "{} {} {}".format(":first_place:", grid_result[0], emoji_list[grid_result[0]]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {} {}".format(":second_place:", grid_result[1], emoji_list[grid_result[1]]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {} {}".format(":third_place:", grid_result[2], emoji_list[grid_result[2]]), value = '\u200b', inline = True)

        # Rest of the drivers
        for i in range(1, len(grid_result)+1):
            if i > 3:
                last_race_embed.add_field(name = "{}. {} {}".format(i,grid_result[i-1], emoji_list[grid_result[i-1]]), value = '\u200b', inline = False)

        await ctx.send(embed = last_race_embed)


def setup(client):
    client.add_cog(RaceInfo(client))


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