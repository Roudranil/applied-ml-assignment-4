import json
import os
import subprocess

import sys
import time
import unittest

import numpy as np
import pandas as pd
import pytest
import requests

# in order to add the correct path to the system to import score
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.score import MODEL_PATH, load_model_vectoriser, score
from src.utils import get_repo_root


DATA_DIR = os.path.join(get_repo_root(), "data")


class TestFlaskIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.flask_process = subprocess.Popen(["python", "app.py"])
        time.sleep(10)  # allow for the flask server to start
        cls.test_dataset = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))

    def test_flask(self):
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        data = {"text": text.values[0]}
        url = "http://127.0.0.1:5000/score"
        # Convert the data to JSON format
        json_data = json.dumps(data)
        # Set the headers for the request
        headers = {"Content-Type": "application/json"}
        # Send the POST request
        response = requests.post(url, data=json_data, headers=headers)
        if response.status_code != 200:
            pytest.fail("Status code is not 200.")
        if "prediction" not in response.json():
            pytest.fail("The response does not contain the prediction field.")
        if "propensity" not in response.json():
            pytest.fail("The response does not contain the propensity field.")

    @classmethod
    def tearDownClass(cls):
        # Close Flask app using command line
        cls.flask_process.terminate()
