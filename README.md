# Testing and model serving

This assignment is a part of the Applied ML course of my MSc. Data Science Program at Chennai Mathematical Institute.

## Problem statement

1.  Unit testing
    - In `score.py`, write a function with the following signature that scores a trained model on a text:
      ```python
      def score(
          text: str,
          model: sklearn.estimator,
          threshold: float
      ) -> Tuple[
          prediction: bool,
          propensity: float
      ]
      ```
    - In test.py, write a unit test function `test_score(...)` to test the score function. You may reload and use the best model saved during experiment in `train.ipynb` (in joblib/pkl format) for testing the score function. You may consider the following points to construct your test cases:
      - does the function produce some output without crashing (smoke test)
      - are the input/output formats/types as expected (format test)
      - is prediction value 0 or 1
      - is propensity score between 0 and 1
      - if you put the threshold to 0 does the prediction always become 1
      - if you put the threshold to 1 does the prediction always become 0
      - on an obvious spam input text is the prediction 1
      - on an obvious non-spam input text is the prediction 0
2.  Flask serving
    - In app.py, create a flask endpoint /score that receives a text as a POST request and gives a response in the json format consisting of prediction and propensity
    - In test.py, write an integration test function test_flask(...) that does the following:
      - launches the flask app using command line (e.g. use os.system)
      - test the response from the localhost endpoint
      - closes the flask app using command line
    - In coverage.txt produce the coverage report output of the unit test and integration test using pytest.

## Solutions

1. Unit testing:
   - I have trained and optimised hyperaparameters for a XGBClassifier instance on the entire training dataset with 5 fold stratified cross validation.
   - I saved the best fit model and the TfIdfVectoriser instance after fitting both of them on the entire training dataset.
   - I collected 9 samples of external test data from kaggle to use for the unit tests.
   - In each of the unit test calls, I randomly choose one sample from that test dataset and check the test.
   - For `test_threshold_0` and `test_threshold_1` i check the output on results of all the samples.
   - Screenshot of successful test case runs for `score.py`
   ![Successful test case runs](images/successful-testcase-run-for-score.png)
