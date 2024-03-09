import os
import re
import string
from typing import Tuple

import joblib
from nltk.corpus import stopwords

MODEL_PATH = "../model"


def startstrip(text: str, subtext: str):
    if text.startswith(subtext):
        text = text[len(subtext) :]
    return text


def clean_text(text: str):
    # convert text to lower case to make it easier to do the preprocessing
    text = text.lower()

    # remove the "subject :" from the beginning
    text = startstrip(text, "subject: ")
    text = text.lstrip("subject: ")

    # finding if the mail was a reply to another mail
    text = startstrip(text, "re : ")

    # cleaning the text
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    stopwords_list = stopwords.words("english")
    text = " ".join(word for word in text.split() if word not in stopwords_list)

    return text


def load_model_vectoriser(model_path: str):
    model = joblib.load(os.path.join(model_path, "model.pkl"))
    vectoriser = joblib.load(os.path.join(model_path, "vectoriser.pkl"))
    return model, vectoriser


def score(text: str, model, vectoriser, threshold: float = 0.5) -> Tuple[bool, float]:
    """Returns the prediction and the propensity score for a text input."""
    x = vectoriser.transform([text])
    probabilities = model.predict_proba(x)
    propensity = probabilities[0][1]
    prediction = propensity > threshold
    return prediction, propensity


def main():
    model, vectoriser = load_model_vectoriser(MODEL_PATH)
    texts = [
        "The scholarship amount has been deposited in your account. Thank you.",
        "You account has been hacked. Give me money.",
        "Please submit your assignment.",
        "This email is spam.",
    ]
    for text in texts:
        print(text)
        text = clean_text(text)
        prediction, propensity = score(text, model, vectoriser)
        print("Spam" if prediction else "Not spam")
        print(f"Pr[text is spam] = {propensity}")


if __name__ == "__main__":
    main()
