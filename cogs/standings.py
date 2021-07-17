import discord
from discord.ext import commands
from discord import Embed
import requests
import json

class Standings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "drivers-standings")
    async def drivers_standings(self, ctx):
        d_standings = get_drivers_standings()
        drivers_embed = Embed(title="Drivers Standings", description = "Current Drivers Standings", colour = 0x19c3e1)
        fields = []
        i = 1
        for driver in d_standings:
            fields.append(("#"+str(i),driver, False))
            i += 1
        for text, value, inline in fields:
            drivers_embed.add_field(name = text, value = value, inline = inline)

        await ctx.send(embed = drivers_embed)
        
    @commands.command(name = "constructor-standings")
    async def constructor_standings(self, ctx):
        c_standings_name, c_standings_points = get_constructor_standings()
        constructor_embed = Embed(title="Constructor Standings", description = "Current Constructor Standings", colour = 0x19c3e1)
        fields = []
        i = 1
        for constructor_name, constructor_points in zip(c_standings_name, c_standings_points):
            fields.append(("#{} {}".format(str(i),constructor_name), constructor_points, False))
            i += 1
        for text, value, inline in fields:
            constructor_embed.add_field(name = text, value = value, inline = inline)
        await ctx.send(embed = constructor_embed)

def setup(client):
    client.add_cog(Standings(client))

# returns drivers standings
def get_drivers_standings():
    response = requests.get("http://ergast.com/api/f1/current/driverStandings.json")
    my_json = response.text
    parsed = json.loads(my_json)
    d_standings = []
    for data in parsed["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:

        constructor_name = data["Constructors"][0]["name"]
        family_name = data["Driver"]["familyName"]
        name = data["Driver"]["givenName"]
        points = data["points"]

        d_standings.append("{} {} ({}) Points: {}".format(name, family_name, constructor_name, points))
    return d_standings

# returns two arrasys 1. constructor standings name 2. points of constructor 
def get_constructor_standings():
    response = requests.get("http://ergast.com/api/f1/current/constructorStandings.json")
    my_json = response.text
    parsed = json.loads(my_json)
    c_standings_name = []
    c_standings_points = []
    for item in parsed["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]:
        c_name = ("{}").format(item['Constructor']['name'])
        c_points = ("Points: {}").format(item['points'])
        c_standings_name.append(c_name)
        c_standings_points.append(c_points)
    return c_standings_name, c_standings_points