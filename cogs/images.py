from io import BytesIO
import os
import datetime
from discord.ext import commands
from util.helpers import rainbowify, textify
from PIL import Image, ImageFont, ImageDraw
import requests
import random

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
            username = user.name
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

    @commands.command(pass_context=True)
    async def gayculator(self, ctx, username=None):
        if username:
            user = ctx.message.server.get_member_named(username)
            if user == None:
                await self.bot.say("Sorry! I couldn't find a user named " + username)
                return
            r = requests.get(user.avatar_url, {"size": "16"})
        else:
            username = ctx.message.author.name
            r = requests.get(ctx.message.author.avatar_url, {"size": "16"})

        userval = sum(map(ord, username))

        random.seed(userval)
        percent_gay = random.randrange(0, 200)

        user_avi = Image.open(BytesIO(r.content))

        filename = str(datetime.datetime.now()) + ctx.message.author.name + ".png"
        rainbowify(user_avi, filename)

        user_avi.close()

        rainbowed = textify("{}% gya".format(percent_gay), filename)
        rainbowed.save(filename)
        rainbowed.close()

        await self.bot.send_file(ctx.message.channel, filename)

        os.remove(filename)
    
def setup(bot):
    bot.add_cog(Images(bot))
