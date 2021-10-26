import discord
import os
from discord.embeds import Embed
from discord.ext import commands

#custom !help command class 
class CustomHelp(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self,mapping):
        #mapping is a dictionary of cogs and commands
        help_embed = Embed(title = ":checkered_flag:Command center:checkered_flag:", description = '\u200b', colour = discord.Colour.orange())
        commands = []
        for cog in mapping:
            for command in mapping[cog]:
                commands.append("!"+command.name)
        joined = "\n".join(commands)
        help_embed.add_field(name = 'Available commands', value = joined, inline=False)

        await self.get_destination().send(embed = help_embed)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)


def read_token():
    return os.getenv("TOKEN")

TOKEN = read_token()
client = commands.Bot(command_prefix='!', help_command=CustomHelp())


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
