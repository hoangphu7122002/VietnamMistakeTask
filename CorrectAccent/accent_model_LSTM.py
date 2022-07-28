import json
from collections import Counter
import numpy as np
from helper_function import *
import tensorflow as tf

ALPHABET = list(sorted(set(ALPHABET)))
indexALPHABET = {e: index for index,e in enumerate(ALPHABET)}
data_path = 'CorrectAccent/'
fi = open(data_path + 'data/tudien_don.json', 'r', encoding='utf-8')
data_single = json.load(fi)
singleWord = data_single.keys()

def is_need_accent(digit):
    if isinstance(digit,int):
        return digit in [indexALPHABET[e] for e in ACCENTED_TO_BASE_CHAR_MAP.keys() if ACCENTED_TO_BASE_CHAR_MAP[e] == digit]
    else:
        return digit in [e for e in ACCENTED_TO_BASE_CHAR_MAP.keys() if ACCENTED_TO_BASE_CHAR_MAP[e] == digit]


class CharacterCodec(object):
    def __init__(self, alphabet, maxlen):
        self.alphabet = list(sorted(set(alphabet)))
        self.index_alphabet = dict((c, i) for c,i in indexALPHABET.items())
        self.maxlen = maxlen

    def encode(self, C, maxlen=None):
        maxlen = maxlen if maxlen else self.maxlen
        X = np.zeros((maxlen, len(self.alphabet)))
        for i, c in enumerate(C[:maxlen]):
            X[i, self.index_alphabet[c]] = 1
        return X

    def try_encode(self, C, maxlen=None):
        try:
            return self.encode(C, maxlen)
        except KeyError:
            return None

    def decode(self, X, calc_argmax=True):
        if calc_argmax:
            X = X.argmax(axis=-1)
        return ''.join(self.alphabet[x] for x in X)


class Model(object):
    def __init__(self, config_file = 'CorrectAccent/model/config.json',weights_file = 'CorrectAccent/model/weights.h5',model_file = 'CorrectAccent/model/model.json'):
        with open(config_file) as f:
            self.config = json.load(f)

        self.maxlen = self.config.get('MAXLEN', 32)
        self.invert = self.config.get('INVERT', True)
        self.ngram = self.config.get('NGRAM', 5)
        self.pad_words_input = True
        self.input_codec = CharacterCodec(ALPHABET, self.maxlen)
        self.codec = CharacterCodec(ALPHABET, self.maxlen)
        #self.model = createModel(self.maxlen,tf)
        self.model = tf.keras.models.model_from_json(open(model_file, 'r').read())
        self.model.load_weights(weights_file)

    def guess(self, words):
        text = ' '.join(words)
        text = pad(text, self.maxlen)
        if self.invert:
            text = text[::-1]
        input_vec = self.input_codec.encode(text)
        preds = self.model.predict(np.array([input_vec]), verbose=0)
        #print(preds.shape)
        #print(preds)

        #-----------optimization here-------------
        #print(len(text),len(preds))
        classes_preds = []
        for word,pred in zip(text,preds[0]):
            if is_need_accent(word):
                envolved_char = list(set([indexALPHABET[w] for w in ACCENTED_TO_BASE_CHAR_MAP.keys() if ACCENTED_TO_BASE_CHAR_MAP[w] == word]))
                #envolved_char.append(indexALPHABET[word])

                pred_extract = {i:p for i,p in enumerate(pred) if i in envolved_char}

                max_index = sorted(pred_extract,key = lambda x : pred_extract[x])
                #print(max_index[-1])
                classes_preds.append(max_index[-1])
            else:
                classes_preds.append(indexALPHABET[word])
        #-----------------------------------------
        #classes_preds = np.argmax(preds, axis=-1)
        #print(classes_x[0],len(classes_x))
        #print(classes_preds,len(classes_preds))
        if self.invert:
            classes_preds = classes_preds[::-1]
        return self.codec.decode(classes_preds, calc_argmax=False).strip('\x00')

    def add_accent(self, text):
        # lowercase the input text as we train the model on lowercase text only
        # but we keep the map of uppercase characters to restore cases in output
        is_uppercase_map = [c.isupper() for c in text]
        text = text.lower()

        # for each block of words or symbols in input text, either append the symbols or
        # add accents for words and append them.
        outputs = []
        words_or_symbols_list = re.findall('\w[\w ]*|\W+', text)
        #print('input:', words_or_symbols_list)
        for words_or_symbols in words_or_symbols_list:
            if is_words(words_or_symbols):
                outputs.append(self._add_accent(words_or_symbols))
            else:
                outputs.append(words_or_symbols)
        #print('output:', outputs)
        output_text = ''.join(outputs)

        # restore uppercase characters
        output_text = ''.join(c.upper() if is_upper else c
                              for c, is_upper in zip(output_text, is_uppercase_map))
        return output_text

    def _add_accent(self, phrase):
        grams = list(gen_ngram(phrase.lower(), n=self.ngram, pad_words=self.pad_words_input))
        guessed_grams = list(self.guess(gram) for gram in grams)
        candidates = [Counter() for _ in range(len(guessed_grams) + self.ngram - 1)]
        for idx, gram in enumerate(guessed_grams):
            for wid, word in enumerate(re.split(' +', gram)):
                candidates[idx + wid].update([word])
        output = ' '.join(c.most_common(1)[0][0] for c in candidates if c)
        return output.strip('\x00 ')

def returnRealOutput(test,model):
    get = model.add_accent(test)
    pairs = [(a, b) for a, b in zip(test.split(' '), get.split(' '))]
    realOutput = []
    for a, b in pairs:
        if b in singleWord:
            realOutput.append(b)
        else:
            realOutput.append(a)
    return " ".join(e for e in realOutput)


#meme
a = 5
if __name__ == '__main__':
    model = Model()
    print(returnRealOutput('co chang trai viet len cay',model))