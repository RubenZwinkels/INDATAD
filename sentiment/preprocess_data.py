import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import joblib


def preprocess_data(csv_file):
    df = pd.read_csv(csv_file)
    texts = df['transcript'].astype(str)

    vectorizer = CountVectorizer(stop_words='english')
    X_bow = vectorizer.fit_transform(texts)

    joblib.dump(vectorizer, 'nlp_model.pkl')
    print("Vectorizer opgeslagen als nlp_model.pkl.")

    return X_bow


if __name__ == "__main__":
    preprocess_data("studentset.csv")