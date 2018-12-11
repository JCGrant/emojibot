from flask import Flask, request, abort, Response, render_template, session
from global_constants import *
from matcher import get_best_intent
from predictor import run_prediction
from util import emojify

app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")
app.config['SECRET_KEY'] = "Super Secret"

def error(message):
    abort(Response(message, 400))

@app.route("/")
def index():
    return render_template('index.html')

def get_favourite_emoji():
    return session.get(FAVOURITE_EMOJI, 'You have no favourite emoji set').decode('unicode-escape')

def put_favourite_emoji(entities):
    session[FAVOURITE_EMOJI] = entities['emoji_code'][0]
    return 'OK!'

def perform_action(intent, entities):
    if intent == GET_FAV_EMOJI:
        return get_favourite_emoji()
    elif intent == PUT_FAV_EMOJI:
        return put_favourite_emoji(entities)
    raise KeyError('Invalid intent: {}'.format(intent))

@app.route("/transform")
def transform():
    sentence = request.args.get('s')
    if sentence is None or len(sentence) == 0:
        error('need a non-empty sentence')
    intent, score, entities = get_best_intent(sentence)
    if score >= 0.95:
        return perform_action(intent, entities)
    return emojify(run_prediction(sentence))
