from response_strings import *
from config_logic import *
import discord
from query_utils import getSheetInfo
from discord.ext import commands

TOKEN: str
with open(".token", "r") as f: TOKEN = f.read().strip()

DEFAULT_LANGUAGE_ENTRIES: dict = readEntries()

bot = commands.Bot(
    command_prefix=COMMAND_CHARACTER, 
    case_insensitive=True, 
    intents=discord.Intents.all(),
)

@bot.command(brief="[Admin] Default language for the server to fall back to")
async def deflang(ctx, lang = None):
    server_id = ctx.guild.id
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

@bot.command(brief="Conversation topics for open discussions (B1 and up)")
async def topic(ctx, lang=None):																		
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

    except Exception as e:
        await ctx.send(embed=formatInEmbed(
            Q_TOO_LITTLE_ENTRIES(),
            None,
            f"Currently: {e.args[0]}")
        )

@bot.command(brief="Simple questions for new learners to start writing or talking (A1-A2)")
async def q(ctx, lang=None):																		
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

bot.run(TOKEN)