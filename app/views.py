from flask import request, abort, Response, render_template, session
from app import app
from global_constants import *
from matcher import get_best_intent
from predictor import run_prediction
from util import emojify

def error(message):
    abort(Response(message, 400))

@app.route("/")
def index():
    """Render the React App"""
    return render_template('index.html')

def get_favourite_emoji():
    """Retreive the the favourite Emoji from the session.
    
    Might be upgraded to a Database in the future."""
    return session.get(FAVOURITE_EMOJI, 'You have no favourite emoji set').decode('unicode-escape')

def put_favourite_emoji(entities):
    """Update the favourite Emoji for the session."""
    session[FAVOURITE_EMOJI] = entities['emoji_code'][0]
    return 'OK!'

def perform_action(intent, entities):
    """Simply performs an action depending on the intent."""
    if intent == GET_FAV_EMOJI:
        return get_favourite_emoji()
    elif intent == PUT_FAV_EMOJI:
        return put_favourite_emoji(entities)
    raise KeyError('Invalid intent: {}'.format(intent))

@app.route("/transform")
def transform():
    """Retreives a sentence from the request and first checks if it matches any of the
    symbolic intents.
    
    If it has a high score, we perform an action.
    Otherwise, we emojify the sentence.
    """
    sentence = request.args.get('s')
    if sentence is None or len(sentence) == 0:
        error('need a non-empty sentence')
    intent, score, entities = get_best_intent(sentence)
    if score >= 0.95:
        return perform_action(intent, entities)
    return emojify(run_prediction(sentence))
