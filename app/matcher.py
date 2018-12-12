import re
import string
from global_constants import *

"""These represent intents the user might have in this application.

We choose the intent by matching a sentence against one of the list of tokens
associated with the intent.

The intent with the best match, is the one we choose.
"""
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
    """Returns a regex matcher.

    Matcher returns True, and the matched part of the string as an entity, if it matches a regex.
    Otherwise it returns False and an empty object.
    """
    def matcher(word):
        match = regex_matchers[regex_kind].match(word)
        if match is None:
            return False, {}
        return True, {regex_kind: [match.group(0)]}
    return matcher

def regular_match(regex_tok):
    """Returns an equality matcher.

    Matcher returns (True, {}) if word == regex_tok.
    Otherwise (False, {})

    The empty object is there merely to conform to the matcher pattern.
    """
    def matcher(word):
        word = word.lower()
        word = word.translate(None, string.punctuation)
        return word == regex_tok, {}
    return matcher

def get_matcher(regex_tok):
    """Will decide which matcher to use depending on the regex_tok's structure"""
    if regex_tok.startswith('$'):
        return regex_match(regex_tok.strip('$'))
    return regular_match(regex_tok)


def add_entity(entities, new_entities):
    """Extends an entity object with new entities"""
    for k, v in new_entities.iteritems():
        if k in entities:
            entities[k].extend(v)
        else:
            entities[k] = v
    return entities

def match_score_for_regex(sentence, regex):
    """Will return the number of regex_tokens the sentences matched against (in order),
    and the length of the regex, and any entities we found while matching.    
    """
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
    """Will choose the best intent out of those defined in map_intent_to_regex"""
    sentence = sentence.encode('unicode-escape')
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

