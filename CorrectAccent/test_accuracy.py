from accent_model_LSTM import Model
import pickle
from difflib import SequenceMatcher
from tqdm import tqdm
import numpy as np
import json

fi = open('data/tudien_don.json', 'r', encoding='utf-8')
data_single = json.load(fi)
singleWord = data_single.keys()

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

def test_accuracy():
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    config_file = 'model/config.json'
    weights_file = 'model/weights.h5'
    model_file = 'model/model.json'

    model = Model(config_file = config_file,weights_file = weights_file,model_file = model_file)
    test_path = 'test/sentences.pkl'

    with open(test_path, 'rb') as handle:
        test_data = pickle.load(handle)

    num_correct = 0
    np.random.shuffle(test_data)
    for sen in tqdm(test_data[:100]):
        if similar(returnRealOutput(sen, model),sen) >= 0.8:
            num_correct += 1

    #hello test CI/CD
    #no no no
    assert num_correct/100 >= 0.27