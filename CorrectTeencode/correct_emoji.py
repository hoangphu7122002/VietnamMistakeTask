import json
from difflib import SequenceMatcher

dict_hex = {"\U0001F600": "cười",
  "\U0001F601": "cười nhe răng",
  "\U0001F602": "cười",
  "\U0001F606": "cười",
  "\U0001F608": "nham hiểm",
  "\U0001F60B": "ngon vãi",
  "\U0001F60E": "ngầu chưa",
  "\U0001F60F": "cười nham hiểm",
  "\U0001F610": "bất lực",
  "\U0001F611": "bất lực",
  "\U0001F615": "sao cũng được",
  "\U0001F615": "buồn",
  "\U0001F61F": "lo lắng",
  "\U0001F620": "hổ báo",
  "\U0001F622": "khóc",
  "\U0001F624": "bực bội",
  "\U0001F62B": "mệt mỏi",
  "\U0001F62D": "khóc",
  "\U0001F62E": "ngạc nhiên",
  "\U0001F632": "ngạc nhiên",
  "\U0001F633": "e thẹn",
  "\U0001F634": "ngủ rồi",
  "\U0001F635": "bất ngờ",
  "\U0001F641": "hic hic",
  "\U0001F644": "giả điên",
  "\U0001F924": "thèm quá",
  "\U0001F92A": "lêu lêu",
  "\U0001F92B": "im lặng",
  "\U0001F92C": "nóng giận",
  "\U0001F92D": "mắc cười",
  "\U0001F92E": "mắc ói",
}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
data_path = 'CorrectTeencode/'
#f_hex = open(data_path + 'emoji/Emoji_Hex.json', 'r',encoding='utf-8')
f_symbol = open(data_path + 'emoji/Emoji_KyHieu.json','r',encoding='utf-8')
#data_hex = f_hex.read()
data_symbol = f_symbol.read()

#dict_hex = json.loads(data_hex)
dict_symbol = json.loads(data_symbol)

def fix_hex(sentence):
    output = ""
    t = sentence.split(" ")
    flagHex = 0
    #'\U0001F602'
    keyHex = list(dict_hex.keys())

    for word in t:
        for key in keyHex:
            if key in word:
                output += dict_hex[word] + " "
                flagHex = 1
                break
        if flagHex == 0:
            output += word + " "
        else:
            flagHex = 1

    return output

def fix_symbol(sentence):
    output = ""
    t = sentence.split(" ")
    flagSymbol = 0
    keySymbol = list(dict_symbol.keys())
    for word in t:
        for key in keySymbol:
            if key in word:
                output += dict_symbol[word] + " "
                flagSymbol = 1
                break
        if flagSymbol == 0:
            output += word + " "
        else:
            flagSymbol = 1

    return output

def fix_emoji(sentence):
    return fix_hex(fix_symbol(sentence))

if __name__ == 'main':
    print(fix_emoji('hôm nay tôi vui :) 😂 😂'))

