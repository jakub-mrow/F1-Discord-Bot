import discord
from discord import embeds
from discord.ext import commands
from discord import Embed
import requests
import json

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


    @commands.command(name = "last-race")
    async def last_race(self,ctx):
        grid_result, add_info = get_last_race()
        last_race_embed = Embed(title = "{}!".format(add_info[1]), description = "Round: {} - {}".format(add_info[0], add_info[2]), colour = 0x19c3e1)


        # Top 3 places in Embed 
        last_race_embed.add_field(name = "{} {}".format(":first_place:", grid_result[0]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {}".format(":second_place:", grid_result[1]), value = '\u200b', inline = True)
        last_race_embed.add_field(name = "{} {}".format(":third_place:", grid_result[2]), value = '\u200b', inline = True)

        # All drivers
        for i in range(1, len(grid_result)+1):
            if i > 3:
                last_race_embed.add_field(name = "{}. {}".format(i,grid_result[i-1]), value = '\u200b', inline = False)

        await ctx.send(embed = last_race_embed)


def setup(client):
    client.add_cog(Testing(client))

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