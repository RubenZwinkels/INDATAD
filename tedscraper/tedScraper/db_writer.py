import psycopg2

import api_caller
import db_conn
import db_reader
from db_conn import create_connection
from datetime import datetime
from psycopg2 import Error

def create_table():
    conn = create_connection()
    cur = conn.cursor()

    query = """
 CREATE TABLE IF NOT EXISTS sentiment (
    id SERIAL PRIMARY KEY,
    rating DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS popularity (
    id SERIAL PRIMARY KEY,
    rating DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS date (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP UNIQUE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS video_data(
    video_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255),
    transcription VARCHAR,
    sentiment INT,
    CONSTRAINT fk_sentiment FOREIGN KEY (sentiment) REFERENCES sentiment(id)
);

CREATE TABLE IF NOT EXISTS statistic (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(20), 
    current_likes BIGINT,
    historic_likes BIGINT,
    current_views BIGINT,
    historic_views BIGINT,
    popularity INT,
    date INT,
    CONSTRAINT fk_video FOREIGN KEY (video_id) REFERENCES video_data(video_id),
    CONSTRAINT fk_popularity FOREIGN KEY (popularity) REFERENCES popularity(id),
    CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES date(id)
);
    """
    cur.execute(query)
    conn.commit()
    cur.close()

def insert_video_data_into_db(video_data):
    conn = create_connection()
    cur = conn.cursor()

    insert_query = """
        INSERT INTO video_data (video_id, title, transcription)
        VALUES (%s, %s, %s)
        ON CONFLICT (video_id) DO NOTHING;
        """

    try:
        # Voer de query uit met data uit de video_metadata dictionary
        cur.execute(insert_query, (
            video_data["video_id"],
            video_data["title"],
            video_data["transcript"]
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Fout bij het invoegen van video metadata: {e}")
    finally:
        cur.close()

def drop_tables():
    conn = create_connection()
    cur = conn.cursor()

    query = """
     DROP TABLE IF EXISTS statistic, video_data, sentiment, popularity, date CASCADE;
    """

    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"fout bij het droppen van alle tables: {e}")
    finally:
        cur.close()

def update_video_statistic(video_id):
    conn = create_connection()
    cur = conn.cursor()

    old_video_statistic = db_reader.get_video_statistic(video_id)
    new_video_statistic = api_caller.get_video_statistic(video_id)
    delete_video_statistic(video_id)
    query = """
    INSERT INTO statistic
    (video_id, current_likes, historic_likes, current_views, historic_views)
    VALUES (%s, %s, %s, %s, %s)
    """

    params = (
        video_id,
        new_video_statistic["likes"],
        old_video_statistic["current_likes"],
        new_video_statistic["views"],
        old_video_statistic["current_views"]
    )


    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def delete_video_statistic(video_id):
    conn = create_connection()
    cur = conn.cursor()
    query = f"""
    DELETE FROM statistic WHERE video_id = '{video_id}';
    """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def create_current_timestamp():
    try:
        conn = create_connection()
        cur = conn.cursor()
        current_timestamp = datetime.now()

        query = """
        INSERT INTO date (date)
        VALUES (%s);
        """
        cur.execute(query, (current_timestamp,))
        conn.commit()
        print(f"Timestamp {current_timestamp} created")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def insert_custom_timestamp(custom_date):
    try:
        conn = create_connection()
        cur = conn.cursor()

        if isinstance(custom_date, str):
            custom_date = datetime.strptime(custom_date, "%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO date (date)
        VALUES (%s);
        """
        cur.execute(query, (custom_date,))
        conn.commit()
        print(f"Timestamp {custom_date} created")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()