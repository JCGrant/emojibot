from flask import Flask, request, jsonify
from predictor import run_predictions

app = Flask(__name__)

@app.route("/predict")
def predict():
    sentences = request.args.getlist('s')
    scores = run_predictions(sentences)
    return jsonify(scores)
