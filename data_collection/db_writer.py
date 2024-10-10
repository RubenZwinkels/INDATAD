from data_collection import api_caller, db_reader
import os
from dotenv import load_dotenv
from data_collection.db_conn import create_connection
from datetime import datetime
from popularity import popularity_analyser

def create_table():
    conn = create_connection()
    cur = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS sentiment (
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
        category_id INT,
        CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES date(id),
        CONSTRAINT fk_sentiment FOREIGN KEY (sentiment) REFERENCES sentiment(id)
    );

    CREATE TABLE IF NOT EXISTS statistic (
        id SERIAL PRIMARY KEY,
        video_id VARCHAR(20), 
        likes BIGINT,
        views BIGINT,
        comment_count BIGINT,
        popularity VARCHAR,
        date INT,
        CONSTRAINT fk_video FOREIGN KEY (video_id) REFERENCES video_data(video_id),
        CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES date(id)
    );

    CREATE TABLE IF NOT EXISTS deploy (
        id SERIAL PRIMARY KEY,
        time TIMESTAMP DEFAULT NOW(),
        script_duration_in_s INTEGER,
        host VARCHAR
    );
        
    CREATE TABLE IF NOT EXISTS tags (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    );
    CREATE TABLE IF NOT EXISTS video_tags (
        video_id VARCHAR(20),
        tag_id INT,
        CONSTRAINT fk_video FOREIGN KEY (video_id) REFERENCES video_data(video_id),
        CONSTRAINT fk_tag FOREIGN KEY (tag_id) REFERENCES  tags(id),
        PRIMARY KEY (video_id, tag_id)
    );

    """
    cur.execute(query)
    conn.commit()
    cur.close()


def insert_video_data_into_db(video_data):
    conn = create_connection()
    cur = conn.cursor()

    insert_query = """
        INSERT INTO video_data (video_id, title, transcription, date, category_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (video_id) DO NOTHING;
        """

    try:
        published_at_date = video_data["publishedAt"]
        clean_date = datetime.strptime(published_at_date, "%Y-%m-%dT%H:%M:%SZ").date()
        cur.execute(insert_query, (
            video_data["video_id"],
            video_data["title"],
            video_data["transcript"],
            get_date_id_by_date(clean_date),
            video_data["category_id"]
        ))
        conn.commit()
        insert_video_tags(video_data["video_id"], video_data["tags"])
    except Exception as e:
        conn.rollback()
        print(f"Fout bij het invoegen van video metadata: {e}")
    finally:
        cur.close()

def update_video_statistic(video_id):
    new_video_statistic = api_caller.get_video_statistic(video_id)
    # popularity bepalen
    popularity_label = popularity_analyser.determine_popularity(new_video_statistic)
    print(f"label: {popularity_label}")

    try:
        conn = create_connection()
        cur = conn.cursor()
        query = """
        INSERT INTO statistic
        (video_id, likes, views, date, comment_count)
        VALUES (%s, %s, %s, %s, %s)
        """

        params = (
            video_id,
            new_video_statistic["likes"],
            new_video_statistic["views"],
            get_date_id_by_date(),
            new_video_statistic["comment_count"]
        )
        cur.execute(query, params)
        conn.commit()

    except Exception as e:
        print(f"Fout met video id: {video_id}: {e}")
        conn.rollback()
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
        conn.rollback()
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

def insert_video_tags(video_id, tags):
    conn = create_connection()
    cur = conn.cursor()

    try:
        insert_tag_query = """
        INSERT INTO tags (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id;
        """

        tag_ids = []
        for tag in tags:
            cur.execute(insert_tag_query, (tag,))
            result = cur.fetchone()

            if result:
                tag_id = result[0]
            else:
                # Haal de bestaande tag_id op als het een conflict was (tag bestaat al)
                cur.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                tag_id = cur.fetchone()[0]

            tag_ids.append(tag_id)

        # Stap 2: Voeg de relaties toe tussen video en tags in `video_tags`-tabel
        insert_video_tag_query = """
        INSERT INTO video_tags (video_id, tag_id)
        VALUES (%s, %s)
        ON CONFLICT (video_id, tag_id) DO NOTHING;
        """
        for tag_id in tag_ids:
            cur.execute(insert_video_tag_query, (video_id, tag_id))

        conn.commit()
        print(f"Tags voor video {video_id} succesvol toegevoegd.")

    except Exception as e:
        conn.rollback()
        print(f"Fout bij het invoegen van tags voor video {video_id}: {e}")

    finally:
        cur.close()
        conn.close()

def insert_popularity(video_data, date_id):
    print(f"video data in insert pop: {video_data}")
    pop_rating = popularity_analyser.determine_popularity(video_data)
    if pop_rating == 1:
        pop_label = "populular"
    else:
        pop_rating = "unpopular"
    query = f"""
    UPDATE statistic
    SET popularity = {pop_label}
    WHERE video_id = {video_data["video_id"]}
    AND date = {date_id}
    """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"error bij insert_popularity: {e}")
    finally:
        cur.close()
        conn.close()

