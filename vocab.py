"""
generates definitions from vocab words
"""
import time
import requests
import creds


def get_word(word):
    headers = {
        'content-type': 'application/json',
        'app_id': creds.APP_ID,
        'app_key': creds.APP_KEY,
    }
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{word}'
    return requests.get(
        url.format(word=word),
        headers=headers,
    )


def parse_definition(word, response):
    try:
        res = response.json()
        res = res.get('results', [])
        for i in ['lexicalEntries', 'entries', 'senses', 'definitions']:
            res = [inner for values in res for inner in values.get(i, [])]
        if res == []:
            print(word)
            print(response)
            print(response.json())
        return res
    except:
        print(word)
        print(response)
        return []


def get_definition(word):
    return parse_definition(word, get_word(word))


def main():
    file = open('words', "r")
    file2 = open("definitions", "w")
    count = 0
    for line in file:
        word = str(line).strip()
        words = word.split("")

        if len(words) > 1:  # manual definitions
            word = words[0]
            definition = " ".join(words[1:])
            print(f'{word}\t{definition}', file=file2)
            continue

        if count >= 50:  # adhering to rate limits
            print("sleeping for 60 seconds")
            time.sleep(60)
            print("resuming")
            count = 0

        count += 1
        defs = get_definition(word)
        if defs == []:
            print(f'{word}\tERROR', file=file2)
        else:
            cur = defs[0]
            print(f'{word}\t{cur}', file=file2)
