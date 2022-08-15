from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
from tqdm import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import underthesea
import tensorflow as tf

def cleaning_text(text, keep_punct=True):
    if keep_punct:
        return re.sub(u'[^{Latin}0-9[:punct:]]+', u' ', text)
    return re.sub(u'[^{Latin}0-9]+', u' ', text)

def standardize_data(sentence):
    row = re.sub(r"[\.,\?]+$-","",sentence)
    row = row.replace(",", " ").replace(".", " ") \
        .replace(";", " ").replace("“", " ") \
        .replace(":", " ").replace("”", " ") \
        .replace('"', " ").replace("'", " ") \
        .replace("!", " ").replace("?", " ") \
        .replace("-", " ").replace("?", " ")
    row = row.strip().lower()
    return row

def load_bert():
    v_phobert = AutoModel.from_pretrained("vinai/phobert-base")
    v_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
    return v_phobert, v_tokenizer
phobert, tokenizer = load_bert()

def phobert_embed_sentence(padded, mask, model=phobert):
    # embed a single setence data
    # param padded: a tokenized, padded sentence
    # param mask: an attention mask of the padded sentence
    padded = torch.tensor(padded).to(torch.long)
    mask = torch.tensor(mask)
    with torch.no_grad():
        last_hidden_states = model(input_ids=padded, attention_mask=mask)[0]
    vector = last_hidden_states[:, 0, :].numpy()  # [:,0,:] to get embedding vector of the first output token [CLS]
    return vector.flatten()


def phobert_embed_data(data, tokenizer=tokenizer):
    # embed the whole dataset with phobert
    # param padded_data: tokenized, padded dataset
    # param mask_data: attention masks of the padded dataset
    MAX_LENGTH = tokenizer.model_max_length  # phobert default max sequence length = 256

    embedded_data = np.array([])
    for line in tqdm(data):
        tokenized_line = tokenizer.encode(line, max_length=MAX_LENGTH, truncation=True)
        # pad sentence to a pre-defined max length, no truncating since it is already truncated in the phobert tokenizing
        padded_line = pad_sequences([tokenized_line], maxlen=MAX_LENGTH, padding='post', value=1)
        # Get attention mask from padded sentence of data to make PhoBERT focus on non-padded data only
        # pad tokenized sentence with value = 1, since 1 is pre-defined padding value of PhoBERT
        mask = np.where(padded_line == 1, 0, 1)

        embedded_line = phobert_embed_sentence(padded_line, mask)

        if embedded_data.shape[0] == 0:
            embedded_data = np.empty((0, embedded_line.shape[0]), 'float32')

        embedded_data = np.concatenate((embedded_data, [embedded_line]))
    return embedded_data

def load_stopwords(stopwords_path = 'predictEmotion/stopwords'):
    sw = []
    with open(stopwords_path, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        sw.append(line.replace("\n",""))
    return sw


sw = load_stopwords()


def preprocessing(text, keep_punct=True):
    text = standardize_data(text)
    # text = remove_emoji(text)
    # tokenize
    line = underthesea.word_tokenize(text)

    # filter stopword
    filter_words = [word for word in line if word not in sw]
    # concat
    line = "".join(text)
    line = underthesea.word_tokenize(line, format="text")

    return cleaning_text(line)

