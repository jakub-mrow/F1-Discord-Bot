import discord
from discord.ext import commands
from discord import Embed
import requests
import json

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