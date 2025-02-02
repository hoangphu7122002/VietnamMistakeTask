from CorrectTeencode.correct_teencode import correct_teencode,correct_short_word_sent, correct_teencode_word
from CorrectTeencode.correct_close_character import correct_close_character_sent
from CorrectTeencode.correct_telex import TelexErrorCorrector
from CorrectTeencode.correct_vni import VniErrorCorrector
from CorrectTeencode.correct_emoji import fix_emoji
import json
import re
data_path = 'CorrectTeencode/'
telexCorrector = TelexErrorCorrector()
vniCorrector = VniErrorCorrector()
region = open(data_path + 'region/southNorth.json','r',encoding = 'utf-8')
fi = open(data_path + 'data/tudien_don.json', 'r', encoding='utf-8')
dictionary = json.load(fi)
dict_region = json.load(region)
southNorthError = dict_region.values()
correctSNE = dict_region.keys()
SNE_dict = {a : b for a,b in zip(southNorthError,correctSNE)}

def southNorthProcess(sent):
    sent = sent.lower()
    words = sent.split(' ')
    output = []
    for word in words:
        if word in southNorthError:
            output.append(SNE_dict[word])
        else:
            output.append(word)
    return ' '.join(e for e in output)

def preprocess(sent):
    sent = sent.lower()
    sent = re.sub(r'[;,.?:\=\+\|!]', r' ', sent)
    sent = re.sub('\n', '', sent)
    sent = re.sub(r'\s+', r' ', sent)
    sent = re.sub(r'^\s', '', sent)
    sent = re.sub(r'\s$', '', sent)
    return sent

def in_dictionary(word):
    try:
        return dictionary[word] != 0
    except:
        return False

def use_correct_func(sent, func):
    words = sent.split()
    ls = []
    for word in words:
        new_word = func(word)
        if not in_dictionary(new_word):
            new_word = word
        ls.append(new_word)
    return ' '.join(ls)

def correct_sent(sent):
    sent = fix_emoji(sent)
    sent = preprocess(sent)
    sent = correct_short_word_sent(sent)
    sent = use_correct_func(sent, telexCorrector.fix_telex_word)
    sent = use_correct_func(sent, vniCorrector.fix_vni_sentence)
    sent = use_correct_func(sent, correct_teencode_word)
    sent = use_correct_func(sent, vniCorrector.fix_vni_sentence)
    sent = use_correct_func(sent, telexCorrector.fix_telex_word)

    sent = correct_close_character_sent(sent)
    sent = southNorthProcess(sent)

    return sent

if __name__ == "__main__":
    sent = 'Có hỗ trơk đổi k shop ơi met65 quas roi62 nũng :))))'
    print(correct_sent(sent))
    # print(in_dictionary('facebook'))