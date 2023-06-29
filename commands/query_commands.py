from config_logic import getDefaultLanguage, readUserScores, saveUserScores
from query_utils import NotEnoughWords, getPresetFromSheet, getQFromSheet
from response_strings import *
from config import GLOBAL_DEFAULT_LANGUAGE, TOPIC_SHEET, Q_SHEET, ANTONYM_SHEET
from globals import DEFAULT_LANGUAGE_ENTRIES, BOT
from discord.ext import commands

async def reportNotEnoughWords(ctx, e):
    await ctx.send(embed=formatInEmbed(
        Q_TOO_LITTLE_ENTRIES(),
        None,
        f"Currently: {e.args[0]}")
    )

async def command_topic(ctx: commands.Context, lang=None):																		
    assert ctx.guild
    lang = lang \
        or getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, str(ctx.guild.id)) \
        or GLOBAL_DEFAULT_LANGUAGE

    try:
        items, names = getQFromSheet(lang, TOPIC_SHEET, ["C", "D"])						
        await ctx.send(embed=formatInEmbed(
            items[0], 
            None,
            f"{names[1]}: {items[1]}")
        )

    except NotEnoughWords as e:
        await reportNotEnoughWords(ctx, e)

    except Exception as e:
        print(e)

async def command_q(ctx: commands.Context, lang=None):																		
    assert ctx.guild
    lang = lang \
        or getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, str(ctx.guild.id)) \
        or GLOBAL_DEFAULT_LANGUAGE

    try:
        items, names = getQFromSheet(lang, Q_SHEET, ["C", "E", "D"])						
        await ctx.send(embed=formatInEmbed(
            items[0], 
            names[2]+":\n ||"+items[2]+"||",
            f"{names[1]}: {items[1]}")
        )

    except NotEnoughWords as e:
        await reportNotEnoughWords(ctx, e)

async def command_quiz(ctx: commands.Context, times: int, lang=None):
    assert ctx.guild
    lang = lang \
        or getDefaultLanguage(DEFAULT_LANGUAGE_ENTRIES, str(ctx.guild.id)) \
        or GLOBAL_DEFAULT_LANGUAGE

    preset: str

    presets = getPresetFromSheet("Q", ANTONYM_SHEET, ["A", "B"])
    if lang in presets: preset = presets[lang]
    else: raise Exception("Language not found")

    wordsAlreadyAsked: list[str] = []
    score: int = 0
    user = ctx.author

    def nextEntry() -> tuple[str, list[str]]:
        while True:
            data, _ = getQFromSheet(
                lang, 
                ANTONYM_SHEET, 
                ["C", "F", "G", "H", "I", "J"] #C is word, rest are possible answers
            )
            word = data[0]
            answers = data[1:]
            if word not in wordsAlreadyAsked: break
        return word, answers

    async def nextQuestion(word: str, answers: list[str]) -> bool: #shouldCount and rightAnswer
        try: word, answers = nextEntry()
        except NotEnoughWords as e: 
            await reportNotEnoughWords(ctx, e)
            raise e
        except Exception as e: 
            raise e
            
        await ctx.send(preset.replace("$1", f"**{word}**"))

        def check(m): 
            isSameAuthor = ctx.author == m.author
            isSameChannel = ctx.channel == m.channel
            return isSameAuthor and isSameChannel

        tryNum = 0
        while True:
            try: 
                response: discord.Message = await BOT.wait_for('message', timeout=60, check=check)
            except TimeoutError: 
                await ctx.send("You took too long to answer :(")
                return False
            except Exception as e: 
                raise e

            if response.content.lower() in answers:
                await ctx.send("Hooray!")
                return True
            else:
                tryNum += 1
                if tryNum == 3:
                    await ctx.send("Aww :(")
                    return False 
                await ctx.send("No sorry :( Try again")

    def addPoints() -> str:
        user_id = str(user.id)
        entries = readUserScores()
        if user_id not in entries: entries[user_id] = 0
        entries[user_id] = int(entries[user_id]) + score
        saveUserScores(entries)
        return entries[user_id]

    for _ in range(times):
        word, answers = nextEntry()
        try: correct = await nextQuestion(word, answers)
        except Exception as e: return print(e)
        if correct: score += 1
    current_score = addPoints()

    await ctx.send(f"You earned {score} point{'s'*int(score > 1)}. Your score is now {current_score}.")