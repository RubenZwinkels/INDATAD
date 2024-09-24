import psycopg2
import api_caller
import db_reader
import os
from dotenv import load_dotenv
from db_conn import create_connection
from datetime import datetime

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
        date DATE UNIQUE DEFAULT CURRENT_DATE
    );

    CREATE TABLE IF NOT EXISTS video_data(
        video_id VARCHAR(20) PRIMARY KEY,
        title VARCHAR(255),
        transcription VARCHAR,
        sentiment INT,
        date INT,
        CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES date(id),
        CONSTRAINT fk_sentiment FOREIGN KEY (sentiment) REFERENCES sentiment(id)
    );

    CREATE TABLE IF NOT EXISTS statistic (
        id SERIAL PRIMARY KEY,
        video_id VARCHAR(20), 
        likes BIGINT,
        views BIGINT,
        popularity INT,
        date INT,
        CONSTRAINT fk_video FOREIGN KEY (video_id) REFERENCES video_data(video_id),
        CONSTRAINT fk_popularity FOREIGN KEY (popularity) REFERENCES popularity(id),
        CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES date(id)
    );

    CREATE TABLE IF NOT EXISTS deploy (
        id SERIAL PRIMARY KEY,
        time TIMESTAMP DEFAULT NOW(),
        script_duration_in_s INTEGER,
        host VARCHAR
    );
    """
    cur.execute(query)
    conn.commit()
    cur.close()


def insert_video_data_into_db(video_data):
    conn = create_connection()
    cur = conn.cursor()

    insert_query = """
        INSERT INTO video_data (video_id, title, transcription, date)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (video_id) DO NOTHING;
        """

    try:
        cur.execute(insert_query, (
            video_data["video_id"],
            video_data["title"],
            video_data["transcript"],
            get_date_id_by_date(video_data["publishedAt"])
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
    try:
        conn = create_connection()
        cur = conn.cursor()

        new_video_statistic = api_caller.get_video_statistic(video_id)

        query = """
        INSERT INTO statistic
        (video_id, likes, views, date)
        VALUES (%s, %s, %s, %s)
        """

        params = (
            video_id,
            new_video_statistic["likes"],
            new_video_statistic["views"],
            get_date_id_by_date()
        )
        cur.execute(query, params)
        conn.commit()

    except Exception as e:
        print(f"Fout met video id: {video_id}: {e}")
    finally:
        cur.close()
        conn.close()


def insert_custom_date(custom_date=None):
    try:
        conn = create_connection()
        cur = conn.cursor()

        if not custom_date:
            custom_date = datetime.now().date()

        if isinstance(custom_date, str):
            custom_date = custom_date.rstrip('Z')
            custom_date = datetime.strptime(custom_date, "%Y-%m-%dT%H:%M:%S").date()

        query = """
        INSERT INTO date (date)
        VALUES (%s)
        RETURNING id;
        """
        cur.execute(query, (custom_date,))

        inserted_id = cur.fetchone()[0]

        conn.commit()
        print(f"Date {custom_date} inserted with ID {inserted_id}")

        return inserted_id

    except Exception as e:
        print(f"Datum al bestaand in db: {e}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def get_date_id_by_date(date=None):
    if date is None:
        date = datetime.now().date()
    excisting_id = db_reader.get_id_by_date(date)

    if excisting_id is None:
        new_id = insert_custom_date(date)
        return new_id
    else:
        return excisting_id


def insert_deploy(duration):
    load_dotenv()
    host = os.environ['HOST']
    rounded_duration = round(duration, 0)

    conn = create_connection()
    cur = conn.cursor()
    query = f"""
    INSERT INTO deploy
    (script_duration_in_s, time, host)
    VALUES ({rounded_duration},
    NOW() AT TIME ZONE 'Europe/Amsterdam',
    '{host}'
    );
    """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()