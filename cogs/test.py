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

def setup(client):
    client.add_cog(Testing(client))
