from discord import Permissions, Embed, Color
from discord.ext import commands
from util import config

import traceback
import time

class Admin():
    """
    Commands for logging, managing channels, managing permissions, etc etc.
    """
    def __init__(self, bot):
        self.bot = bot
        self.conf = config.Config()
        self.logging_settings = {
            "log_user_join": True,
            "log_user_remove": True,
            "log_user_ban": True,
            "log_message_delete": False,
            "log_message_edit": False
        }

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def logging(self, ctx):
        """
        A group of commands dealing with logging
        Requires the "Manage Channels" permission.
        """
        if ctx.invoked_subcommand is None:
            await self.bot.say(
                """
                usage: `logging [option] [arguments]`
                see `j.help logging` for details.
                """
            )

    @logging.command(pass_context=True)
    async def set_channel(self, ctx):
        server_id = ctx.message.server.id
        try:
            self.conf.settings["servers"][server_id]["logging_channel"] = ctx.message.channel.id
            self.conf.settings["servers"][server_id]["logging_settings"] = self.logging_settings
            self.conf.save()
        except ValueError:
            self.conf.settings["servers"][server_id] = {
                "logging_channel" : ctx.message.channel.id,
                "logging_settings" : self.logging_settings
                }
            self.conf.save()

        await self.bot.say("This channel will now be used to log moderator messages.")

    @logging.error
    async def set_logging_error(self, error, ctx):
        if isinstance(error, commands.CheckFailure):
            await self.bot.say("You require the \"manage channels\" permission to use this command.")
        else:
            tb = traceback.format_tb(error.__traceback__)
            print(type(error))
            print(error.__cause__)
            print(''.join(tb))

    @logging.command(pass_context = True)
    async def settings(self, ctx):
        join_emb = self._create_help_emb("Log when members join?", 
                                        self._bool_to_yn(self.logging_settings["log_user_join"]))
        remove_emb = self._create_help_emb("Log when members are removed?",  
                                        self._bool_to_yn(self.logging_settings["log_user_remove"]))
        ban_emb = self._create_help_emb("Log when members are banned?",  
                                        self._bool_to_yn(self.logging_settings["log_user_ban"]))

        join = await self.bot.say(embed=join_emb)
        await self.bot.add_reaction(join, "✅")
        await self.bot.add_reaction(join,"🚫" )
        remove = await self.bot.say(embed=remove_emb)
        await self.bot.add_reaction(remove, "✅")
        await self.bot.add_reaction(remove,"🚫" )
        ban = await self.bot.say(embed=ban_emb)
        await self.bot.add_reaction(ban, "✅")
        await self.bot.add_reaction(ban,"🚫" )


        res_join = await self.bot.wait_for_reaction(["✅", "🚫"], message=join, user=ctx.message.author,
                                                    timeout=1000)
        res_remove = await self.bot.wait_for_reaction(["✅", "🚫"], message=remove, user=ctx.message.author,
                                                    timeout=1000)
        res_ban = await self.bot.wait_for_reaction(["✅", "🚫"], message=ban, user=ctx.message.author,
                                                    timeout=1000)

        await self._resolve_help_settings(res_join, "log_user_join", join)
        await self._resolve_help_settings(res_ban, "log_user_ban", ban)
        await self._resolve_help_settings(res_remove, "log_user_remove", remove)

    def _create_help_emb(self, name, current):
        emb = Embed()
        emb.title = "Option"
        emb.add_field(name=name, value="Currently: **" + current + "**")
        emb.colour = Color.light_grey()

        return emb

    async def _resolve_help_settings(self, result, option, message):
        if result.reaction == "✅":
            self.logging_settings[option] = True
        else:
            self.logging_settings[option] = False

        emb = Embed()
        emb.colour = Color.green()
        emb.title = "{0} set to {1.reaction.emoji}".format(option, result)
        await self.bot.edit_message(message, embed=emb)
        await self.bot.clear_reactions(message)

    def _bool_to_yn(self, boolean):
        return "y" if boolean else "n"

def setup(bot):
    bot.add_cog(Admin(bot))