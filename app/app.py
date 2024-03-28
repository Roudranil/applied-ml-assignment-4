from flask import Flask
from flask_restful import Api

from resources.score import Score

app = Flask(__name__)
api = Api(app)

api.add_resource(Score, "/score")

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
