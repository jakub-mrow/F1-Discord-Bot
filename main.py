import discord
import os
from discord.ext import commands

def read_token():
    with open("token.txt", "r") as file:
        lines = file.readlines()
        return lines[0].strip()

TOKEN = read_token()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('F1 fan!'))
    print("Bot is ready!")

@client.command()
async def load(ctx, extension):
    client.load_extension("cogs.{}".format(extension))

@client.command()
async def unload(ctx, extension):
    client.unload_extension("cogs.{}".format(extension))

@client.command()
async def reload(ctx, extension):
    client.unload_extension("cogs.{}".format(extension))
    client.load_extension("cogs.{}".format(extension))

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension("cogs.{}".format(file[:-3]))


client.run(TOKEN)
