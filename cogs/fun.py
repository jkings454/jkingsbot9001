from discord.ext import commands
import random
import requests

class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self):
        """
        gay
        """
        gays = [
            "very much so",
            "a suprise, for sure, but a welcome one",
            "full homo",
            "who isn't tbh",
            "yup that's me",
            "god im so gay",
            "gay me daddy",
            "yea"
            ]
        await self.bot.say(random.choice(gays))

    @commands.command()
    async def pupper(self):
        reddit_data = requests.get("https://reddit.com/r/rarepuppers.json")

def setup(bot):
    bot.add_cog(Fun(bot))