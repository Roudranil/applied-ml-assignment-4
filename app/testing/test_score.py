import os
import sys
import unittest

import numpy as np
import pandas as pd
import pytest

# in order to add the correct path to the system to import score
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.score import MODEL_PATH, load_model_vectoriser, score


class TestScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.model, cls.vectoriser = load_model_vectoriser(MODEL_PATH)
        cls.test_dataset = pd.read_csv(
            "/data/cmi/notes/sem-4/applied-ml/assignments/assignment-3/data/test.csv"
        )

    def test_smoketest(self):
        """test if score(text, model, vectoriser, threshold) produces some output
        without crashing"""
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        try:
            score(text.values[0], self.model, self.vectoriser)
        except Exception as e:
            pytest.fail(f"function call failed due to exception {e}")
        pass

    def test_format(self):
        """test if the score(text, model, vectoriser, threshold) output is of the
        form Tuple[bool, float]"""
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        result = score(text.values[0], self.model, self.vectoriser)
        if not isinstance(result, tuple):
            pytest.fail(f"Output {result} is not of type Tuple[Bool, Float].")
        if result[0] != 0 and result[0] != 1:
            pytest.fail(
                f"{result[0]} is not of type Bool.\n{result} is not of type Tuple[Bool, Float]"
            )
        if not isinstance(result[1], float):
            pytest.fail(
                f"{result[1]} is not of type Float.\n{result} is not of type Tuple[Bool, Float]"
            )

    def test_prediction_range(self):
        """test if score(text, model, vectoriser, threshold) output prediction is 0
        or 1 (or True or False)"""
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        result = score(text.values[0], self.model, self.vectoriser)
        if result[0] != 0 and result[0] != 1:
            pytest.fail(f"Prediction {result[0]} is neither True nor False.")

    def test_propensity_range(self):
        """test if score(text, model, vectoriser, threshold) output propensity is a
        value between 0 and 1"""
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        result = score(text.values[0], self.model, self.vectoriser)
        if not 0 <= result[1] <= 1:
            pytest.fail(f"Propensity {result[1]} is not between 0 and 1.")

    def test_threshold_0(self):
        """test if setting threshold to 0 always produces all results as true"""
        texts = self.test_dataset.loc[:, "text"]
        for text in texts:
            prediction, _ = score(text, self.model, self.vectoriser, 0)
            if prediction != 1:
                pytest.fail(
                    "Setting threshold to 0 does not result in all True prediction"
                )

    def test_threshold_1(self):
        """test if setting threshold to 1 always produces all results as false"""
        texts = self.test_dataset.loc[:, "text"]
        for text in texts:
            prediction, _ = score(text, self.model, self.vectoriser, 1)
            if prediction != 0:
                pytest.fail(
                    "Setting threshold to 1 does not result in all False prediction"
                )

    def test_obvious_spam(self):
        text = "Hello. This email is spam"
        prediction, _ = score(text, self.model, self.vectoriser)
        if prediction == 0:
            pytest.fail(f"Obvious spam email\n---\n{text}\n---\nmisclassified as ham")

    def test_obvious_non_spam(self):
        text = "Dear students, please submit your assignments before the deadline. You will be graded on this."
        prediction, _ = score(text, self.model, self.vectoriser)
        if prediction == 1:
            pytest.fail(
                f"Obvious non spam email\n---\n{text}\n---\nmisclassified as ham"
            )
