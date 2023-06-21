from config_logic import getDefaultLanguage
from query_utils import NotEnoughWords, getSheetInfo
from response_strings import *
from config import GLOBAL_DEFAULT_LANGUAGE, TOPIC_SHEET, Q_SHEET
from globals import DEFAULT_LANGUAGE_ENTRIES, BOT
from discord.ext import commands

async def topic(ctx: commands.Context, lang=None):																		
    assert ctx.guild
    lang = lang \
        or getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, ctx.guild.id) \
        or GLOBAL_DEFAULT_LANGUAGE

    try:
        items, names = getSheetInfo(lang, TOPIC_SHEET, ["C", "D"])						
        await ctx.send(embed=formatInEmbed(
            items[0], 
            None,
            f"{names[1]}: {items[1]}")
        )

    except NotEnoughWords as e:
        await ctx.send(embed=formatInEmbed(
            Q_TOO_LITTLE_ENTRIES(),
            None,
            f"Currently: {e.args[0]}")
        )

    except Exception as e:
        print(e)

async def q(ctx: commands.Context, lang=None):																		
    assert ctx.guild
    lang = lang \
        or getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, ctx.guild.id) \
        or GLOBAL_DEFAULT_LANGUAGE

    try:
        items, names = getSheetInfo(lang, Q_SHEET, ["C", "E", "D"])						
        await ctx.send(embed=formatInEmbed(
            items[0], 
            names[2]+":\n ||"+items[2]+"||",
            f"{names[1]}: {items[1]}")
        )

    except Exception as e:
        await ctx.send(embed=formatInEmbed(
            Q_TOO_LITTLE_ENTRIES(),
            None,
            f"Currently: {e.args[0]}")
        )