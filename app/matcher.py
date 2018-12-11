import re
import string
from global_constants import *

map_intent_to_regex = [
    (GET_FAV_EMOJI, [
        ['my', 'favourite', 'emoji'],
        ['emoji', 'my', 'favourite'],
        ['what', 'my', 'favourite', 'emoji'],
        ['what', 'emoji', 'my', 'favourite'],
        ['which', 'my', 'favourite', 'emoji'],
        ['which', 'emoji', 'my', 'favourite'],
    ]),
    (PUT_FAV_EMOJI, [
        ['my', 'favourite', 'emoji', '$emoji_code'],
        ['$emoji_code', 'my', 'favourite', 'emoji'],
        ['$emoji_code', 'emoji', 'my', 'favourite'],
    ]),
]

regex_matchers = {
    'emoji_code': re.compile(r'\\(u|U)[0-9a-fA-F]+')
}

def regex_match(regex_kind):
    def matcher(word):
        match = regex_matchers[regex_kind].match(word)
        if match is None:
            return False, None
        return True, {regex_kind: match.group(0)}
    return matcher

def regular_match(regex_tok):
    def matcher(word):
        return word == regex_tok, {}
    return matcher

def get_matcher(regex_tok):
    if regex_tok.startswith('$'):
        return regex_match(regex_tok.strip('$'))
    return regular_match(regex_tok)


def add_entity(entities, new_entities):
    for k, v in new_entities.iteritems():
        if k in entities:
            entities[k].append(v)
        else:
            entities[k] = [v]
    return entities

def match_score_for_regex(sentence, regex):
    words = sentence.split()
    i = 0
    len_regex = len(regex)
    all_entities = {}
    for word in words:
        regex_tok = regex[i]
        matcher = get_matcher(regex_tok)
        match, entities = matcher(word)
        if match:
            i += 1
            all_entities = add_entity(all_entities, entities)
            if i >= len_regex:
                break
    return i, len_regex, all_entities

def get_best_intent(sentence):
    sentence = sentence.encode('unicode-escape')
    # Strip all punctuation
    sentence = sentence.translate(None, string.punctuation)
    sentence = sentence.lower()
    best_score = 0
    best_intent = None
    best_length = 0
    best_entities = {}
    for intent in map_intent_to_regex:
        intent_name, regexes = intent
        for regex in regexes:
            score, len_regex, entities = match_score_for_regex(sentence, regex)
            if score > best_score and len_regex >= best_length:
                best_score = score
                best_intent = intent_name
                best_length = len_regex
                best_entities = entities
    if best_length == 0:
        return None, 0, {}
    return best_intent, 1.0 * best_score / best_length, entities

