from commands import admin_commands
from commands import query_commands
from globals import TOKEN, BOT
import discord
from discord.ext import commands

@BOT.command(brief="[Admin] Default language for the server to fall back to")
async def deflang(ctx, lang = None): await admin_commands.deflang(ctx, lang)

@BOT.command(brief="Conversation topics for open discussions (B1 and up)")
async def topic(ctx, lang=None): await query_commands.topic(ctx, lang)

@BOT.command(brief="Simple questions for new learners to start writing or talking (A1-A2)")
async def q(ctx, lang=None): await query_commands.q(ctx, lang)

@BOT.command(brief="Test quiz.")
async def quiz(ctx: commands.Context):
    "THIS IS A TEST COMMAND"
    user: discord.Member | discord.User = ctx.author

    await ctx.send("Say yes.")

    def check(m): return ctx.author == m.author
    try: 
        response: discord.Message = await BOT.wait_for('message', timeout=60, check=check)
    except TimeoutError: 
        return await ctx.send("You took too long to answer :(")
    except Exception as e: 
        return print(e)

    if response.content.lower() == "yes":
        await ctx.send("Hooray!")
    else:
        await ctx.send("Aww :(")

BOT.run(TOKEN)