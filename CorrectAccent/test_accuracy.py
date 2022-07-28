from accent_model_LSTM import *
import pickle
from difflib import SequenceMatcher
from tqdm import tqdm
import numpy as np

def test_accuracy():
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    config_file = 'CorrectAccent/model/config.json'
    weights_file = 'CorrectAccent/model/weights.h5'
    model_file = 'CorrectAccent/model/model.json'

    model = Model(config_file = config_file,weights_file = weights_file,model_file = model_file)
    test_path = 'CorrectAccent/test/sentences.pkl'

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