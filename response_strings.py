import discord

def Q_TOO_LITTLE_ENTRIES():
    return "Language must have more than 30 entries."

def Q_NO_DEFAULT_LANGUAGE(): 
    return "No default language is set"

def Q_DEFAULT_LANGUAGE_IS(default_language: str): 
    return f"The default language of this server is {default_language}"

def Q_NO_PERMS_LANG(): 
    return "You have to be an administrator to change the default language of a server"

def Q_DEFAULT_LANG_SET(default_language: str):
    return f"The default language has been set to `{default_language}`"

def formatInEmbed(title: str, desc: str|None, footer: str) -> discord.Embed:
    return discord.Embed(
        title=title,
        description=desc,
    ).set_footer(text=footer)