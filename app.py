from flask import Flask, request, abort, Response
from predictor import run_prediction
from util import emojify

app = Flask(__name__)

def error(message):
    abort(Response(message, 400))

@app.route("/predict")
def predict():
    sentence = request.args.get('s')
    if sentence is None or len(sentence) == 0:
        error('need a non-empty sentence')
    return emojify(run_prediction(sentence))
