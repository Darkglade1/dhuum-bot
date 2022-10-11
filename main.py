# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import google.cloud.texttospeech as tts
import os

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