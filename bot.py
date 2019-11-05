# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def find_guild():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    return guild


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to ' + GUILD + '!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'what up {member.name}, welcome to {GUILD}!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command(name='hello')
async def command_hello(ctx):
    response = f'hello {ctx.author.name}!'
    await ctx.send(response)


@bot.command(name='hehwo')
async def command_hehwo(ctx):
    response = f'hehwo {ctx.author.name}-kun!! UwU *nuzzles your neckie* (^-^)'
    await ctx.send(response)


@bot.command(name='server_members')
async def print_server_members(ctx):
    members = '\n - '.join([member.name for member in find_guild().members])
    response = f'{GUILD}:\n - {members}'
    await ctx.send(response)


bot.run(TOKEN)
