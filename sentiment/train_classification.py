import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report
import joblib


def train_model(csv_file):
    # Laad de gegevens
    df = pd.read_csv(csv_file)
    texts = df['transcript'].astype(str)
    labels = df['label']  # Zorg ervoor dat dit je labels zijn

    # Verdeel de data
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Laad de opgeslagen vectorizer
    vectorizer = joblib.load('nlp_model.pkl')

    # Transformeer de tekst naar Bag of Words
    X_train_bow = vectorizer.transform(X_train)
    X_test_bow = vectorizer.transform(X_test)

    # Classificatie Model: Naive Bayes
    model = MultinomialNB()
    model.fit(X_train_bow, y_train)

    # Voorspellingen maken
    predictions = model.predict(X_test_bow)

    # Evaluatie
    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))

    # Sla het model op als classificatie_model.pcl
    joblib.dump(model, 'classificatie_model.pkl')
    print("Model opgeslagen als classificatie_model.pkl.")


if __name__ == "__main__":
    train_model("studentset.csv")