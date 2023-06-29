from commands import admin_commands
from commands import query_commands
from globals import TOKEN, BOT
from discord.ext import commands

@BOT.command(brief="[Admin] Default language for the server to fall back to")
async def deflang(ctx, lang = None): await admin_commands.command_deflang(ctx, lang)

@BOT.command(brief="Conversation topics for open discussions (B1 and up)")
async def topic(ctx, lang=None): await query_commands.command_topic(ctx, lang)

@BOT.command(brief="Simple questions for new learners to start writing or talking (A1-A2)")
async def q(ctx, lang=None): await query_commands.command_q(ctx, lang)

@BOT.command(brief="Test quiz.")
async def quiz(ctx: commands.Context, *args): 
    lang = None
    times = 5

    if len(args) > 1:
        assert isinstance(args[0], str)
        if not args[0].isnumeric(): lang = args[0]
        else: 
            times = int(args[0])
            if len(args) > 1: lang = args[1]

    await query_commands.command_quiz(ctx, times, lang)

BOT.run(TOKEN)