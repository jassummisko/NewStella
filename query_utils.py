from config_logic import *
import urllib.request as urlrequest
import urllib.parse as urlparse
import json
import random

class NotEnoughWords(Exception): pass

def getPresetFromSheet(sheet: str, link: str, quer: list[str]|str) -> dict:
    query="select "+", ".join(quer)
    t = urlrequest.urlopen("https://docs.google.com/spreadsheets/d/"+link+"/gviz/tq?sheet="+sheet+"&tq="+urlparse.quote_plus(query))
    data = json.loads(t.read()[47:-2])["table"]

    returnDict = {}
    for entry in data["rows"]:
        lang = entry['c'][0]['v']
        preset = entry['c'][1]['v']
        if preset != None:
            returnDict[lang] = preset

    return returnDict

def getQFromSheet(sheet: str, link: str, quer: list[str]|str) -> tuple[list[str], list[str]]:		#Define function getTopic with "sheet" as an argument (this corresponds to the language code)
    if type(quer) == str: quer = [quer]

    amount_of_words = len(quer)			#get amount of items queried
    query="select "+", ".join(quer)

    items = []
    names = []
    amount_of_entries: int = 0
    amount_of_questions: int = 0

    t = urlrequest.urlopen("https://docs.google.com/spreadsheets/d/"+link+"/gviz/tq?sheet="+sheet+"&tq="+urlparse.quote_plus(query))

    #Have to do this because there's some noise that google adds to their request
    data = json.loads(t.read()[47:-2])["table"]

    #If the row corresponding to the generated number is empty, regenerate the number
    amount_of_entries = len(data["rows"])
    for i in range(amount_of_entries):
        if data["rows"][i]["c"][0] is not None:
            amount_of_questions += 1

    if amount_of_questions < 30: raise NotEnoughWords(amount_of_questions)

    if amount_of_questions > 1: rnd = random.randrange(0, amount_of_questions - 1)
    else: rnd = 0

    #Gets questions off each row and appends them to items. Yes it's noisy
    for i in range(amount_of_words):
        try: items.append(data["rows"][rnd]["c"][i]["v"] or "/")
        except: items.append("/")

    #Get word for "Question" and "Category" in the selected language from the sheet
    for i in range(amount_of_words):
        try: names.append(data["cols"][i]["label"] or "/")
        except: names.append("/")

    return items, names