import joblib
import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import StandardScaler


def determine_popularity(video_data):
    # Controleer of belangrijke velden aanwezig zijn
    if video_data["likes"] is None or video_data["comment_count"] is None or video_data['date'] is None:
        print("determine_popularity: likes of comments niet beschikbaar dus automatisch unpopular")
        return 0

    # Zet de data om naar een DataFrame en schaal deze
    df = convert_to_dataframe(video_data)
    df = scale_dataframe(df)

    # Label bepalen met het model
    label = assign_label(df)

    if label is None:
        print("determine_popularity: geen label kunnen toewijzen")
        return 0
    return label


def load_scaler():
    try:
        # Voor wanneer deze functie vanuit deze file wordt aangeroepen
        scaler = joblib.load('scaler.save')
    except FileNotFoundError:
        try:
            # Voor wanneer deze functie vanuit de main wordt aangeroepen
            scaler = joblib.load('./popularity/scaler.save')
        except FileNotFoundError:
            print("Error: Scaler file niet gevonden.")
            return None
    return scaler


def load_model():
    try:
        # Voor wanneer deze functie vanuit deze file wordt aangeroepen
        model = joblib.load('popularity_model.pkl')
    except FileNotFoundError:
        try:
            # Voor wanneer deze functie vanuit de main wordt aangeroepen
            model = joblib.load('./popularity/popularity_model.pkl')
        except FileNotFoundError:
            print("Error: Popularity model niet gevonden.")
            return None
    return model


def calculate_title_length(title):
    if title:
        return len(title)
    return 0


def extract_date_info(date):
    if date:
        year = date.year
        month = date.month
        day = date.day
        return year, month, day
    return None, None, None


def convert_to_dataframe(data_dict):
    today = datetime.date.today()
    days_since_published = (today - data_dict['date']).days

    if days_since_published == 0:
        days_since_published = 1

    formatted_data = {
        'views': [float(data_dict['views'])],
        'likes': [float(data_dict['likes'])],
        'comment_count': [int(data_dict['comment_count'])],
        'engagement_rate': [float(data_dict['likes'] / data_dict['views'])],
        'views_over_time': [int(data_dict['views'] / days_since_published)]
    }

    df = pd.DataFrame(formatted_data)
    return df


def scale_dataframe(df):
    scaler = load_scaler()
    if scaler is None:
        print("Error: Scaler niet geladen.")
        return df

    columns = ["views", "likes", "comment_count", "engagement_rate", "views_over_time"]
    df[columns] = scaler.transform(df[columns])

    return df


def assign_label(df):
    model = load_model()
    if model is None:
        print("Error: Model niet geladen.")
        return None

    label = model.predict(df)
    return label[0]