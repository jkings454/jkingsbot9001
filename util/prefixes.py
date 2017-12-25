import discord
from util import config

conf = config.Config()

def get_prefix(bot : discord.ext.commands.Bot, message : discord.Message):
    prefix = ["j."]
    if message.author.id in conf.settings["users"]:
        try:
            prefix.append(conf.settings["users"][message.author.id]["prefix"])
        except Exception as ex:
            pass
    try:
        prefix.append(conf.settings["servers"][message.server.id]["prefix"])
    except Exception as ex:
        pass

    return discord.ext.commands.when_mentioned_or(*prefix) (bot, message)

def get_user_prefix(user : discord.User):
    try:
        return conf.settings["users"][user.id]["prefix"]
    except KeyError:
        conf.settings["users"][user.id] = {
            "prefix": None
        }
        conf.save()
        return None

def get_server_prefix(server : discord.Server):
    try:
        return conf.settings["servers"][server.id]["prefix"]
    except KeyError:
        conf.settings["servers"][server.id] = {
            "prefix": None
        }
        conf.save()
        return None

def set_user_prefix(user : discord.User, prefix : str):
    try:
        conf.settings["users"][user.id]["prefix"] = prefix
        conf.save()
    except KeyError:
        conf.settings["users"][user.id] = {
            "prefix": prefix
        }
        conf.save()

def set_server_prefix(server : discord.Server, prefix : str):
    try:
        conf.settings["servers"][server.id]["prefix"] = prefix
        conf.save()
    except KeyError:
        conf.settings["servers"][server.id] = {
            "prefix": prefix
        }
        conf.save()