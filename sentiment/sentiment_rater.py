import joblib
import numpy as np


def determine_sentiment(text):
    # model en vectorizer laden
    model = load_model()
    vectorizer = load_vectorizer()

    # tekst omzetten naar een TF-IDF matrix met de geladen vectorizer
    text_vector = vectorizer.transform([text])  # zorg voor een 2d-array met TF-IDF waarden

    # sentiment voorspellen op basis van de getransformeerde tekst
    sentiment_rating = model.predict(text_vector)

    if sentiment_rating[0] == 0:
        return "negatief"
    elif sentiment_rating[0] == 1:
        return "positief"
    else:
        print(f"sentiment rater returnt: {sentiment_rating[0]}. Dit is niet 1 of 0 dus help.")
        return None


def load_model():
    try:
        # als het wordt uitgelezen uit folder sentiment
        model = joblib.load("classificatie_model.pkl")
    except FileNotFoundError:
        # als het wordt uitgelezen uit main
        model = joblib.load("./sentiment/classificatie_model.pkl")
    return model

def load_vectorizer():
    try:
        # als het wordt uitgelezen uit folder sentiment
        vectorizer = joblib.load("nlp_model.pkl")
    except FileNotFoundError:
        # als het wordt uitgelezen uit main
        vectorizer = joblib.load("./sentiment/nlp_model.pkl")
    return vectorizer

if __name__ == "__main__":
    test_text = "A Palestinian and an Israeli, Face to Face | Aziz Abu Sarah and Maoz Inon | TED"
    determine_sentiment(test_text)