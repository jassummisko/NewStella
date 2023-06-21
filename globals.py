from config import COMMAND_CHARACTER
from config_logic import readEntries
import discord
from discord.ext.commands import Bot as DiscordBot

TOKEN: str
with open(".token", "r") as f: TOKEN = f.read().strip()

DEFAULT_LANGUAGE_ENTRIES: dict = readEntries()

BOT = DiscordBot(
    command_prefix=COMMAND_CHARACTER, 
    case_insensitive=True, 
    intents=discord.Intents.all(),
)