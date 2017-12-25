from discord.ext import commands

import random

class Rng():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choice(self, *choices):
        """
        Makes a hard choice for you.
        """
        if not choices:
            await self.bot.say("Hold on cowboy you need to give me some options to choose from.")
            return
        sayings = [
            "I think {} sounds more gay", 
            "go with {}", "as a doctor, i'd recommend {}",
            "{} is the way",
            "please, {}, all the way"
            ]
        await self.bot.say(random.choice(sayings).format(random.choice(choices)))

def setup(bot):
    bot.add_cog(Rng(bot))