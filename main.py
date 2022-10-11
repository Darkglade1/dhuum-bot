# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import google.cloud.texttospeech as tts
import os
import mechanics
import json

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def sab(ctx, *argv):
    f = open("bosses/sab.json")
    data = json.load(f)
    boss_mechanics = data["mechanics"]
    time_limit = data["timeLimit"]
    for mechanic_data in boss_mechanics:
        print(mechanic_data)
        mechanic = mechanics.from_json_data(mechanic_data, time_limit)
        mechanics_map = mechanic.get_time_to_message_dict(argv)
        for result in mechanics_map:
            print(result, mechanics_map[result])
    f.close()
    await ctx.send("test")


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


@bot.command()
async def list_languages(ctx):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    await ctx.send(f" Languages: {len(languages)} ".center(60, "-"))


bot.run('MTAyOTEzMDYwMzAwMzY1MDA2OQ.G2LcN1.b_6Yfiw3T4ryRaqAEj5lWrshXBzhOD2BCS45o0')