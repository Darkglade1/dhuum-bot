import discord
from discord.ext import tasks
import time

ready_message = "3, 2, 1, go!"


class MechanicTask:
    def __init__(self, ctx, total_list):
        self.ctx = ctx
        self.total_list = total_list
        self.start_time = 0

    def start_mechanics(self):
        global ready_message
        self.say(ready_message)
        time.sleep(2)  # 2 seconds is how long it takes for the bot to say the ready message
        self.start_time = time.time()
        self.check_mechanics.start()

    def stop_mechanics(self):
        self.check_mechanics.cancel()

    @tasks.loop(seconds=1.0)
    async def check_mechanics(self):
        if len(self.total_list) > 0:
            passed_time = time.time() - self.start_time
            for mechanics_list in self.total_list:
                mechanic = mechanics_list[0]
                print(mechanic)
                if passed_time >= mechanic[0]:
                    succeeded = self.say(mechanic[1])
                    if succeeded:
                        del mechanics_list[0]
                if len(mechanics_list) == 0:
                    self.total_list.remove(mechanics_list)

    def say(self, message):
        filename = f"audio/{message}.wav"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
        try:
            self.ctx.voice_client.play(source)
            return True
        except discord.ClientException:
            return False

