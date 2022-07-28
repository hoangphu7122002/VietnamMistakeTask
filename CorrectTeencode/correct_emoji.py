import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
data_path = 'CorrectTeencode/'
f_hex = open(data_path + 'emoji/Emoji_Hex.json', 'r',encoding='utf-8')
f_symbol = open(data_path + 'emoji/Emoji_KyHieu.json','r',encoding='utf-8')
data_hex = f_hex.read()
data_symbol = f_symbol.read()

dict_hex = json.loads(data_hex)
dict_symbol = json.loads(data_symbol)

def fix_hex(sentence):
    output = ""
    #t = sentence.split(" ")
    flagHex = 0
    #'\U0001F602'
    keyHex = list(dict_hex.keys())
    for word in sentence:
        x = str(hex(int(format(ord(word)))))[2:].upper()
        if x in keyHex:
            output += dict_hex[x]
        else:
            output += word

    return output

def fix_symbol(sentence):
    output = ""
    t = sentence.split(" ")
    flagSymbol = 0
    keySymbol = list(dict_symbol.keys())
    for word in t:
        for key in keySymbol:
            if key in word:

                output += dict_symbol[key] + " "
                flagSymbol = 1
                break
        if flagSymbol == 0:
            output += word + " "

    return output

def fix_emoji(sentence):
    return fix_hex(fix_symbol(sentence))

if __name__ == '__main__':
    print(fix_emoji('hôm nay tôi vui 😀 quá đi á'))
