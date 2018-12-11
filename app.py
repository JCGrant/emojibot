from flask import Flask, request, abort, Response, render_template
from predictor import run_prediction
from util import emojify

app = Flask(__name__, template_folder="client/build", static_folder="client/build/static")

def error(message):
    abort(Response(message, 400))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict")
def predict():
    sentence = request.args.get('s')
    if sentence is None or len(sentence) == 0:
        error('need a non-empty sentence')
    return emojify(run_prediction(sentence))
