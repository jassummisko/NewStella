from config_logic import *
import urllib.request
import urllib.parse
import json
import random

class NotEnoughWords(Exception): pass

def getSheetInfo(sheet: str, link: str, quer: list[str]|str) -> tuple[list[str], list[str]]:		#Define function getTopic with "sheet" as an argument (this corresponds to the language code)
    urlopen = urllib.request.urlopen

    if type(quer) == str: quer = [quer]

    amount_of_words = len(quer)			#get amount of items queried
    query="select "+", ".join(quer)

    items = []
    names = []
    amount_of_entries: int = 0
    amount_of_questions: int = 0

    t = urlopen("https://docs.google.com/spreadsheets/d/"+link+"/gviz/tq?sheet="+sheet+"&tq="+urllib.parse.quote_plus(query))

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
        try:
            items.append(data["rows"][rnd]["c"][i]["v"] or "/")
            print(str(i)+": "+data["rows"][rnd]["c"][i]["v"])
        except:
            items.append("/")
            print(str(i)+": /")

    #Get word for "Question" and "Category" in the selected language from the sheet
    for i in range(amount_of_words):
        try: names.append(data["cols"][i]["label"] or "/")
        except: names.append("/")

    return items, names