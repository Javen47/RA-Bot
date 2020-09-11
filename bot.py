# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from ASCII_art import ASCII_weebs, ASCII_patrick, ASCII_communism
from check_in_config import CHECK_IN_QUESTIONS_FIRST_YEARS, CHECK_IN_QUESTIONS_RETURNERS, CHECK_IN_HEADER_MESSAGE, \
    CHECK_IN_NUMBER, CHECK_IN_QUESTIONS_SECOND_YEARS, CHECK_IN_QUESTIONS_THIRD_YEARS, CHECK_IN_QUESTIONS_FOURTH_YEARS

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
MAINTENANCE_EMAIL = os.getenv('MAINTENANCE_EMAIL')

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

    message.content = message.content.lower()

    # disable listeners
    if message.content == 'ra done':
        if message.author in listening_student_year_user_list:
            listening_student_year_user_list.remove(message.author)
        if message.author in listening_check_in_data_user_list:
            listening_check_in_data_user_list.remove(message.author)
        print(f'{message.author} has finished with their check-in.')
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

@bot.command(name='author', help='Gives info about the developer and the link to the project')
async def command_hello(ctx):
    response = f'\nHello, my name is Javen, an RA at MTU, and am the creator of this bot.\nIf you would like to use ' \
               f'this bot for your own discord server, you can find the project at my GitHub ' \
               f'account:\nhttps://github.com/Javen47/RA-Bot'
    await ctx.send(response)


@bot.command(name='weebs')
async def command_weebs(ctx):
    response = ASCII_weebs
    await ctx.send(response)


@bot.command(name='motherland')
async def command_mother_land(ctx):
    response = ASCII_communism
    await ctx.send(response)


@bot.command(name='commie')
async def command_commie(ctx):
    response = ASCII_patrick
    await ctx.send(response)


@bot.command(name='repair', help='Gives info on maintenance requests')
async def command_repair(ctx):
    response = f'Do you need something fixed by maintenance?\nSend an email to: [{MAINTENANCE_EMAIL}].\nMake sure to ' \
               f'include the location of the problem, what the problem is, when you would like it fixed. '
    await ctx.send(response)


@bot.command(name='hello')
async def command_hello(ctx):
    response = f'hello {ctx.author.name}!'
    await ctx.send(response)


@bot.command(name='hehwo')
async def command_hehwo(ctx):
    response = f'hehwo {ctx.author.name}-kun!! UwU *nuzzles your neckie* (^-^)'
    await ctx.send(response)


@bot.command(name='uwu')
async def command_uwu(ctx):
    response = 'UwU *kisses and nuzzles your neckie* (^-^)'
    await ctx.send(response)


@bot.command(name='check-in', help='Begins your check-in through Discord')
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
        response = prepare_check_in_questions(CHECK_IN_QUESTIONS_FIRST_YEARS, message.author)
    elif message.content == 'second-year':
        response = prepare_check_in_questions(CHECK_IN_QUESTIONS_SECOND_YEARS, message.author)
    elif message.content == 'third-year':
        response = prepare_check_in_questions(CHECK_IN_QUESTIONS_THIRD_YEARS, message.author)
    elif message.content == 'fourth-year':
        response = prepare_check_in_questions(CHECK_IN_QUESTIONS_FOURTH_YEARS, message.author)
    else:
        response = 'Are you a first-year, second-year, third-year, or fourth-year?'
        if message.author not in listening_student_year_user_list:
            listening_student_year_user_list.append(message.author)

    await message.author.dm_channel.send(response)


@bot.command(name='oops')
async def command_oops(ctx):
    response = 'OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo!' \
              ' The code monkeys at our headquarters are working VEWY HAWD to fix this!'
    await ctx.send(response)


@bot.command(name='list-members', help='Shows all the members of the server')
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


def write_check_in_question(author, question):
    file = open(f'check-ins/{CHECK_IN_NUMBER}-{author}.txt', 'a')
    file.write(question)
    file.close()


def prepare_check_in_questions(check_in_questions, message_author):
    response = ''
    index = 1
    for question in check_in_questions:
        formatted_question = str(index) + '.) ' + question + '\n'
        response += formatted_question
        write_check_in_question(message_author, formatted_question)
        index = index + 1
    if message_author not in listening_check_in_data_user_list:
        listening_check_in_data_user_list.append(message_author)
    write_check_in_question(message_author, '\n')
    response += '\nType the command "ra done" when you are finished.'

    return response


# Run Script
bot.run(TOKEN)
