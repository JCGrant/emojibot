# -*- coding: utf-8 -*-

""" Use DeepMoji to score texts for emoji distribution.
The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the DeepMoji repo.
"""
from __future__ import print_function, division
import json
import numpy as np
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.model_def import deepmoji_emojis
from deepmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH


def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


maxlen = 30
batch_size = 32

print('Loading model from {}.'.format(PRETRAINED_PATH))
model = deepmoji_emojis(maxlen, PRETRAINED_PATH)
model.summary()
model._make_predict_function()

print('Building tokenizer using dictionary from {}'.format(VOCAB_PATH))
with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
st = SentenceTokenizer(vocabulary, maxlen)


def run_predictions(sentences):
    tokenized, _, _ = st.tokenize_sentences(sentences)

    prob = model.predict(tokenized)

    # Find top emojis for each sentence. Emoji ids (0-63)
    # correspond to the mapping in emoji_overview.png
    # at the root of the DeepMoji repo.
    scores = []
    for i, s in enumerate(sentences):
        t_score = {}
        t_score['sentence'] = s
        t_prob = prob[i]
        ind_top = top_elements(t_prob, 5)
        t_score['ids'] = ind_top.tolist()
        t_score['id_probs'] = t_prob[ind_top].tolist()
        t_score['sum_id_probs'] = sum(t_prob[ind_top])
        scores.append(t_score)
    return scores

