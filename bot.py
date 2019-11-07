# bot.py
import os
import time
from random import randint

import discord
from dotenv import load_dotenv
from discord.ext import commands

from check_in_config import CHECK_IN_QUESTIONS_FIRST_YEARS, CHECK_IN_QUESTIONS_RETURNERS, CHECK_IN_HEADER_MESSAGE,\
    CHECK_IN_NUMBER

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# Listening variables. If enabled, on_message will redirect message to the listener's respective function.
listening_student_year_user_list = []
listening_check_in_data_user_list = []


#########################################
# Events
#########################################


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

    global listening_student_year_user_list
    global listening_check_in_data_user_list

    # disable listeners
    if message.content == 'ra done':
        if message.author in listening_student_year_user_list:
            listening_student_year_user_list.remove(message.author)
        if message.author in listening_check_in_data_user_list:
            listening_check_in_data_user_list.remove(message.author)
        await message.author.create_dm()
        await message.author.dm_channel.send('Thank you!')
        return

    # if bot is in listening for student year mode for student
    if message.author in listening_student_year_user_list:
        if str(message.channel) == f'Direct Message with {message.author}':
            await command_check_in_message(message)

    # if bot is in listening for check-in data mode for student and is in a DM channel
    if message.author in listening_check_in_data_user_list:
        if str(message.channel) == f'Direct Message with {message.author}':
            return write_check_in(message)

    await bot.process_commands(message)

    if str(message.channel) == f'Direct Message with {message.author}':
        if message.author not in listening_check_in_data_user_list:
            if message.author not in listening_student_year_user_list:
                await message.author.create_dm()
                await message.author.dm_channel.send('You are not in check-in mode. Type "ra check-in" to begin.')


###########################################################
# Commands
###########################################################


@bot.command(name='hello')
async def command_hello(ctx):
    response = f'hello {ctx.author.name}!'
    await ctx.send(response)


@bot.command(name='hehwo')
async def command_hehwo(ctx):
    response = f'hehwo {ctx.author.name}-kun!! UwU *nuzzles your neckie* (^-^)'
    await ctx.send(response)


@bot.command(name='king')
async def command_king(ctx):
    response = 'He who possesses the most tide pods, holds the most respect. '
    await ctx.send(response)


@bot.command(name='check-in')
async def command_check_in_ctx(ctx):
    global listening_student_year_user_list
    if ctx.message.author in listening_student_year_user_list:
        return
    print(f'\n{ctx.message.author} has started their check-in.')
    await command_check_in_message(ctx.message)


async def command_check_in_message(message):
    await message.author.create_dm()
    global listening_student_year_user_list
    global listening_check_in_data_user_list

    if message.author in listening_check_in_data_user_list:
        return
    if message.author not in listening_student_year_user_list:
        await message.author.dm_channel.send(CHECK_IN_HEADER_MESSAGE)
        await message.author.dm_channel.send('-')
    else:
        listening_student_year_user_list.remove(message.author)

    response = ''
    if message.content == 'first-year':
        for question in CHECK_IN_QUESTIONS_FIRST_YEARS:
            response += question
            if message.author not in listening_check_in_data_user_list:
                listening_check_in_data_user_list.append(message.author)
    elif message.content == 'returner':
        for question in CHECK_IN_QUESTIONS_RETURNERS:
            response += question
            if message.author not in listening_check_in_data_user_list:
                listening_check_in_data_user_list.append(message.author)
    else:
        response = 'Are you a first-year or returner?'
        if message.author not in listening_student_year_user_list:
            listening_student_year_user_list.append(message.author)

    await message.author.dm_channel.send(response)


@bot.command(name="trivia")
async def command_trivia(ctx):
    response = 'pls trivia'
    await ctx.send(response)
    answer = randint(1, 4)
    time.sleep(2)
    await ctx.send(answer)


@bot.command(name='oops')
async def command_oops(ctx):
    response = 'OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo!' \
              ' The code monkeys at our headquarters are working VEWY HAWD to fix this!'
    await ctx.send(response)


@bot.command(name='list-members')
async def print_server_members(ctx):
    members = '\n - '.join([member.name for member in find_guild().members])
    response = f'{GUILD}:\n - {members}'
    await ctx.send(response)


###################################################
# Helper Functions
###################################################


def find_guild():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    return guild


def write_check_in(message):
    file = open(f'check-ins/{CHECK_IN_NUMBER}-{message.author}.txt', 'a')
    file.write(message.content + '\n')
    file.close()


# Run Script
bot.run(TOKEN)
