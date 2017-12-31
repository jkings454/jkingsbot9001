from io import BytesIO
import os
import datetime
from discord.ext import commands
from util.rainbowify import rainbowify
from PIL import Image
import requests

class Images():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def gayvatar(self, ctx, username = None):
        """
        Puts a rainbow overlay on an avatar.
        """
        if username:
            user = ctx.message.server.get_member_named(username)
            if user == None:
                await self.bot.say("Sorry! I couldn't find a user named " + username)
                return
            r = requests.get(user.avatar_url)
        else:
            r = requests.get(ctx.message.author.avatar_url)
            
        user_avi = Image.open(BytesIO(r.content))
        filename = str(datetime.datetime.now()) + ctx.message.author.name + ".png"

        rainbowify(user_avi, filename)

        user_avi.close()

        await self.bot.send_file(ctx.message.channel, filename)

        os.remove(filename)

def setup(bot):
    bot.add_cog(Images(bot))
