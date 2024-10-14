import pandas as pd
import nltk
import ssl
import certifi
from nltk.tokenize import word_tokenize


def main():
    # SSL-configuratie om certifi te gebruiken
    ssl._create_default_https_context = ssl._create_unverified_context
    ssl.create_default_context(cafile=certifi.where())

    # NLTK benodigde pakketten downloaden
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')  # Download de ontbrekende woordenlijst

    # Laad je dataset
    df = pd.read_csv("studentset.csv")

    # Combineer alle tekst in één string
    raw_text = " ".join(df['transcript'].astype(str))
    print(raw_text.len())

    # Voer named entity chunking uit
    ne_tree = nltk.ne_chunk(nltk.pos_tag(word_tokenize(raw_text)))
    print(ne_tree)


if __name__ == "__main__":
    main()