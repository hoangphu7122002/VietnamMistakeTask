from predictEmotion.lib import *

MLP_model = tf.keras.models.load_model("predictEmotion/MLP")

def predict(sentence):
    x = [cleaning_text(sentence)]

    doc = phobert_embed_data(x)
    res = MLP_model.predict(np.array(np.expand_dims(doc, -1)))[0]
    print(res)
    if res[0] > res[1]:
        return "negative"
    return "positive"

def predictBatch(sentences):
    x = [cleaning_text(sen) for sen in sentences]

    doc = phobert_embed_data(x)
    resBatch = MLP_model.predict(np.array(np.expand_dims(doc, -1)))
    resStr = []
    for res in resBatch:
        if res[0] > res[1]:
            resStr.append("negative")
        else:
            resStr.append("positive")
    return resStr

if __name__ == 'main':
    sentence = ["áo này đẹp ghê","tôi không thích chiếc áo này đâu", "cổ tay ko vừa", "dịch vụ khá tốt"]
    print(predictBatch(sentence))

