from io import BytesIO
import datetime
from discord.ext import commands
from util.rainbowify import rainbowify
from PIL import Image
import requests

class Images():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    def gayvatar(self, ctx, user = None):
        if user:
            await self.bot.say("yikes! this isn't quite ready yet!")
        else:
            r = requests.get(ctx.message.author.avatar_url)
            user_avi = Image.open(BytesIO(r.content))
            filename = str(datetime.datetime.now()) + ctx.message.author.name + ".png"

            rainbowify(user_avi, filename)

            user_avi.close()

            
            
