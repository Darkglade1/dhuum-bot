from discord.ext import tasks
import time


class MechanicTask:
    def __init__(self, total_list):
        self.total_list = total_list
        self.start_time = 0

    async def start_mechanics(self, ctx):
        await ctx.send("3, 2, 1, Go!")
        self.start_time = time.time()
        self.check_mechanics.start(ctx)

    def stop_mechanics(self):
        self.check_mechanics.cancel()

    @tasks.loop(seconds=5.0)
    async def check_mechanics(self, ctx):
        if len(self.total_list) > 0:
            passed_time = time.time() - self.start_time
            for mechanics_list in self.total_list:
                mechanic = mechanics_list[0]
                print(mechanic)
                if passed_time >= mechanic[0]:
                    await ctx.send(mechanic[1])
                    del mechanics_list[0]
                if len(mechanics_list) == 0:
                    self.total_list.remove(mechanics_list)