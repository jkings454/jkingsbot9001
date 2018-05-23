import discord
from util.config import Config

class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config()

    async def log_member_join(self, member, channel):
        member_avatar = member.avatar_url if member.avatar_url != None else member.default_avatar_url
        emb = discord.Embed()
        emb.title = "Member Join"
        emb.set_thumbnail(url=member_avatar)
        emb.colour = discord.Color.green()
        emb.add_field(name="Username", value=member.name)
        emb.add_field(name="Join Date", value=str(member.joined_at))

        await self.bot.send_message(channel, embed=emb)

    async def log_member_leave(self, member, channel):
        member_avatar = member.avatar_url if member.avatar_url != None else member.default_avatar_url
        emb = discord.Embed()
        emb.title = "Member Remove"
        emb.set_thumbnail(url=member_avatar)
        emb.colour = discord.Color.red()
        emb.add_field(name="Username", value=member.name)
        emb.add_field(name="Join Date", value=str(member.joined_at))

        await self.bot.send_message(channel, embed=emb)

    async def log_member_ban(self, member, channel):
        member_avatar = member.avatar_url if member.avatar_url != None else member.default_avatar_url
        emb = discord.Embed()
        emb.title = "Member Ban"
        emb.set_thumbnail(url=member_avatar)
        emb.colour = discord.Color.dark_orange()
        emb.add_field(name="Username", value=member.name)
        emb.add_field(name="Join Date", value=str(member.joined_at))

        await self.bot.send_message(channel, embed=emb)