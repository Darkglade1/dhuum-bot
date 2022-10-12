# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import google.cloud.texttospeech as tts
import os
import mechanics
import json
import time
import asyncio
import typing # For typehinting
import functools

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

going = True


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
    total_list = parse_mechanics(data, *argv)
    f.close()
    await start_mechanics(ctx, total_list)
    await ctx.send("test sab")


@bot.command()
async def dhuum(ctx, *argv):
    f = open("bosses/dhuum.json")
    data = json.load(f)
    total_list = parse_mechanics(data, *argv)
    f.close()
    await start_mechanics(ctx, total_list)
    await ctx.send("test dhuum")


@bot.command()
async def stop(ctx):
    global going
    going = False


async def start_mechanics(ctx, total_list):
    global going
    going = True
    loop = asyncio.get_event_loop()
    await ctx.send("3, 2, 1, Go!")
    start_time = time.time()
    while len(total_list) > 0 and going:
        passed_time = time.time() - start_time
        next_mechanic_times = []
        for mechanics_list in total_list:
            mechanic = mechanics_list[0]
            print(mechanic)
            if passed_time >= mechanic[0]:
                await ctx.send(mechanic[1])
                del mechanics_list[0]
            if len(mechanics_list) == 0:
                total_list.remove(mechanics_list)
            mechanic = mechanics_list[0]
            time_to_mechanic = (start_time + mechanic[0]) - time.time()
            next_mechanic_times.append(time_to_mechanic)
        min_time = min(next_mechanic_times)
        print("Sleeping ", min_time)
        time.sleep(min_time)


def parse_mechanics(data, *argv):
    boss_mechanics = data["mechanics"]
    time_limit = data["timeLimit"]
    total_list = []
    for mechanic_data in boss_mechanics:
        mechanic = mechanics.from_json_data(mechanic_data, time_limit)
        mechanics_list = mechanic.get_time_to_message_list(argv)
        total_list.append(mechanics_list)
        for result in mechanics_list:
            text_to_wav(result[1])
    print(total_list)
    return total_list


def text_to_wav(text):
    filename = f"audio/{text}.wav"
    if os.path.isfile(filename):
        return
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"
    language_code = "en-US"
    voice_name = "en-US-Standard-G"
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')


bot.run('MTAyOTEzMDYwMzAwMzY1MDA2OQ.G2LcN1.b_6Yfiw3T4ryRaqAEj5lWrshXBzhOD2BCS45o0')