import unittest
import subprocess
import time
import requests
import json

import numpy as np
import pandas as pd
import pytest


class TestFlaskIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.flask_process = subprocess.Popen(["python", "app.py"])
        time.sleep(10)  # allow for the flask server to start
        cls.test_dataset = pd.read_csv(
            "/data/cmi/notes/sem-4/applied-ml/assignments/assignment-3/data/test.csv"
        )

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
