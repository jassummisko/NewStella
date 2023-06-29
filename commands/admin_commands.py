from globals import *
from config_logic import getDefaultLanguage, addEntry
from discord.ext import commands
from response_strings import *

async def command_deflang(ctx: commands.Context, lang = None):
    assert ctx.guild, "Count not retreive guild"
    assert isinstance(ctx.message.author, discord.Member), "Count not retreive member information"
    server_id = str(ctx.guild.id)
    default_language: str | None

    if not lang: 
        default_language = getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, server_id)
        if not default_language: 
            return await ctx.send(Q_NO_DEFAULT_LANGUAGE())
        else: 
            return await ctx.send(Q_DEFAULT_LANGUAGE_IS(default_language))

    if not ctx.message.author.guild_permissions.administrator:
        return await ctx.send(Q_NO_PERMS_LANG())
    addEntry(DEFAULT_LANGUAGE_ENTRIES, server_id, lang)  
    return await ctx.send(Q_DEFAULT_LANG_SET(lang))