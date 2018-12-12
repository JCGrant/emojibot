# -*- coding: utf-8 -*-
import pytest
import numpy as np

from app.global_constants import *
from app.matcher import *
from app.predictor import *
from app.util import *
from app.views import *
from app import app


# Test predictor.py

def test_top_elements():
    array = np.array([3,4,2,1,10,11,12,13])
    for x, y in zip(top_elements(array, 5), np.array([7,6,5,4,1])):
        assert x == y


# Test matcher.py

def test_regex_match():
    tests = [
        {
            'kind': 'emoji_code',
            'word': 'hello',
            'match': False,
            'entities': {},
        },
        {
            'kind': 'emoji_code',
            'word': '\U0001f602',
            'match': True,
            'entities': {'emoji_code': ['\U0001f602']},
        },
        {
            'kind': 'emoji_code',
            'word': '\u2665',
            'match': True,
            'entities': {'emoji_code': ['\u2665']},
        },
    ]
    for test in tests:
        assert regex_match(test['kind'])(test['word']) == (test['match'], test['entities'])

def test_regular_match():
    tests = [
        {
            'regex_tok': 'what',
            'word': 'hello',
            'match': False,
            'entities': {},
        },
        {
            'regex_tok': 'what',
            'word': 'what',
            'match': True,
            'entities': {},
        },
    ]
    for test in tests:
        assert regular_match(test['regex_tok'])(test['word']) == (test['match'], test['entities'])

def test_add_entity():
    tests = [
        {
            'entities': {},
            'new_entities': {},
            'out': {},
        },
        {
            'entities': {},
            'new_entities': {'colors': ['red', 'blue']},
            'out': {'colors': ['red', 'blue']},
        },
        {
            'entities': {'colors': ['red', 'blue']},
            'new_entities': {},
            'out': {'colors': ['red', 'blue']},
        },
        {
            'entities': {},
            'new_entities': {'emoji_code': ['\u2665']},
            'out': {'emoji_code': ['\u2665']},
        },
        {
            'entities': {'colors': ['red']},
            'new_entities': {'colors': ['blue']},
            'out': {'colors': ['red', 'blue']},
        },
    ]
    for test in tests:
        assert add_entity(test['entities'], test['new_entities']) == test['out']

def test_match_score_for_regex():
    tests = [
        {
            'sentence': 'what is the time',
            'regex': ['what', 'time'],
            'score': 2,
            'len_regex': 2,
            'entities': {},
        },
        {
            'sentence': 'what is the time',
            'regex': ['time', 'what'],
            'score': 1,
            'len_regex': 2,
            'entities': {},
        },
        {
            'sentence': 'what is the time',
            'regex': ['how', 'time', 'what'],
            'score': 0,
            'len_regex': 3,
            'entities': {},
        },
        {
            'sentence': 'I \u2665 you',
            'regex': ['i', '$emoji_code', 'you'],
            'score': 3,
            'len_regex': 3,
            'entities': {'emoji_code': ['\u2665']},
        },
    ]
    for test in tests:
        assert match_score_for_regex(test['sentence'], test['regex']) == \
                (test['score'], test['len_regex'], test['entities'])

def test_get_best_intent():
    tests = [
        {
            'sentence': u'What is my favourite emoji?',
            'best_intent': GET_FAV_EMOJI,
            'score': 1.0,
            'entities': {},
        },
        {
            'sentence': u'Which emoji is my favourite emoji?',
            'best_intent': GET_FAV_EMOJI,
            'score': 1.0,
            'entities': {},
        },
        {
            'sentence': u'my favourite emoji?',
            'best_intent': GET_FAV_EMOJI,
            'score': 1.0,
            'entities': {},
        },
        {
            'sentence': u'emoji favourite my',
            'best_intent': GET_FAV_EMOJI,
            'score': 2.0/3,
            'entities': {},
        },
        {
            'sentence': u'\u2665 is my favourite emoji',
            'best_intent': PUT_FAV_EMOJI,
            'score': 1.0,
            'entities': {'emoji_code': ['\u2665']},
        },
    ]
    for test in tests:
        assert get_best_intent(test['sentence']) == \
                (test['best_intent'], test['score'], test['entities']), \
                test['sentence']


# Test util.py

def test_get_emoji():
    assert get_emoji(0) == '\U0001f602'
    with pytest.raises(KeyError):
        get_emoji(-1)
    with pytest.raises(KeyError):
        get_emoji(64)

def test_emojify():
    tests = [
        {
            'in': {'ids': [1,2,3]},
            'out': u'😒',
        },
        {
            'in': {'ids': [4,5,6]},
            'out': u'😍',
        },
    ]
    for test in tests:
        assert emojify(test['in']) == test['out']

def test_map_id_to_emoji():
    assert len(map_id_to_emoji) == 64
