import joblib
import pandas as pd
import numpy as np
import datetime


def determine_popularity(video_data):
    df = convert_to_dataframe(video_data)
    print(df.info())


def load_scaler():
    try:
        # Voor wanneer deze functie vanuit deze file wordt aangeroepen
        scaler = joblib.load('scaler.save')
    except(FileNotFoundError):
        # Voor wanneer deze functie vanuit de main wordt aangeroepen
        scaler = joblib.load('./popularity/scaler.save')
    finally:
        return scaler


def load_model():
    try:
        # Voor wanneer deze functie vanuit deze file wordt aangeroepen
        model = joblib.load('popularity_model.pkl')
    except(FileNotFoundError):
        # Voor wanneer deze functie vanuit de main wordt aangeroepen
        model = joblib.load('./popularity/popularity_model.pkl')
    finally:
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
    print(df.head())
    return df