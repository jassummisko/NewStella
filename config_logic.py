from config import *
import csv

def readEntries() -> dict:
    entries: dict

    with open(INFO_FILEPATH, "r") as f:
        table = [row for row in csv.reader(f, delimiter=',')]
        entries = {row[0]: row[1] for row in table[1:]}

    return entries

def saveEntries(entries: dict):
    data: str = "Server ID,Language\n"

    for language_id, default_language in entries.items():
        data += f"{language_id},{default_language}\n"

    with open(INFO_FILEPATH, "w") as f: f.write(data)

def addEntry(entries: dict, server_id: str, default_language: str):
    entries[server_id] = default_language
    saveEntries(entries)

def getDefaultLanguage(entries: dict, server_id: str) -> str|None:
    if server_id in entries: return entries[server_id]
    return None

def readUserScores() -> dict:
    entries: dict

    with open(SCORE_FILEPATH, "r") as f:
        table = [row for row in csv.reader(f, delimiter=',')]
        entries = {row[0]: row[1] for row in table[1:]}

    return entries
    
def saveUserScores(entries: dict):
    data: str = "User ID,Score\n"

    for language_id, default_language in entries.items():
        data += f"{language_id},{default_language}\n"

    with open(SCORE_FILEPATH, "w") as f: f.write(data)