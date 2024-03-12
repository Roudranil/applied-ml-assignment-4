from flask import json, request, jsonify
from flask_restful import Resource
from src.score import MODEL_PATH, score, load_model_vectoriser


class Score(Resource):
    def post(self):
        model, vectoriser = load_model_vectoriser(MODEL_PATH)
        text = request.json.get("text")
        print(text)
        if text:
            prediction, propensity = score(text, model, vectoriser, threshold=0.5)
            return jsonify({"prediction": prediction, "propensity": propensity})
        else:
            return jsonify({"error": "No text provided"})
