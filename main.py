import discord
from discord.ext import commands
import google.cloud.texttospeech as tts
import os
import mechanics
import mechanics_task
import json


description = '''MORTALS. COWER IN FEAR AT THE SOUND OF MY VOICE.

THERE IS NO CONCLUSION MORE NATURAL THAN MISSING MECHANICS BECAUSE YOU WEREN'T LISTENING TO ME.'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

task = mechanics_task.MechanicTask(None, None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx. voice_client.disconnect()


@bot.command()
async def start(ctx, boss, *argv):
    filename = f"bosses/{boss}.json"
    f = open(filename)
    data = json.load(f)
    total_list = parse_mechanics(data, *argv)
    f.close()
    global task
    task = mechanics_task.MechanicTask(ctx, total_list)
    task.start_mechanics()


@bot.command()
async def stop(ctx):
    global task
    task.stop_mechanics()


def parse_mechanics(data, *argv):
    text_to_wav(mechanics_task.ready_message)
    boss_mechanics = data["mechanics"]
    time_limit = data["timeLimit"]
    total_list = []
    for mechanic_data in boss_mechanics:
        mechanic = mechanics.from_json_data(mechanic_data, time_limit)
        mechanics_list = mechanic.get_time_to_message_list(argv)
        total_list.append(mechanics_list)
        for result in mechanics_list:
            text_to_wav(result[1])
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
    try:
        os.mkdir("audio/")
    except OSError:
        pass
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')


token_file = "token.json"
token_file = open(token_file)
token_data = json.load(token_file)
token = token_data["token"]
bot.run(token)
