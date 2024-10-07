from data_collection.db_conn import create_connection
from datetime import datetime

def get_video_ids():
    conn = create_connection()
    cur = conn.cursor()
    query = """
    SELECT video_id FROM video_data;
    """
    cur.execute(query)
    dirty_ids = cur.fetchall()
    clean_ids = []

    for (video_id,) in dirty_ids:
        clean_ids.append(clean_video_id(video_id))

    return clean_ids

def clean_video_id(video_id):
    return video_id.strip("',()")

def get_recent_video_statistic(video_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        query = f"""
        SELECT
            vd.video_id,
            vd.title,
            vd.transcription,
            vd.category_id,
            s.likes,
            s.views,
            d.date,
            se.rating AS sentiment_rating,
            ARRAY_AGG(t.name) AS tags
        FROM
            video_data vd
        JOIN
            statistic s ON vd.video_id = s.video_id
        LEFT JOIN
            date d ON s.date = d.id
        LEFT JOIN
            sentiment se ON vd.sentiment = se.id
        LEFT JOIN
            video_tags vt ON vd.video_id = vt.video_id
        LEFT JOIN
            tags t ON vt.tag_id = t.id
        WHERE
            vd.video_id = '04PmEJaYKd0'
        GROUP BY
            vd.video_id, vd.title, vd.transcription, vd.category_id, s.likes, s.views, d.date, se.rating
        ORDER BY
            d.date DESC
        LIMIT 1;
        """
        cur.execute(query)
        data = cur.fetchone()

        if data is None:
            raise ValueError(f"Geen statistieken voor video met id: {video_id} gevonden")

        # Kolommen die overeenkomen met de geretourneerde data
        columns = ['video_id', 'title', 'transcription', 'category_id', 'likes', 'views', 'date', 'sentiment_rating', 'tags']

        # Maak een dictionary van de resultaten
        data_dict = dict(zip(columns, data))

        print(data_dict)
        return data_dict

    except Exception as e:
        print(e)
        return None

    except Exception as e:
        print(e)
        return {
            "video_id": video_id,
            "title": None,
            "transcription": None,
            "category_id": None,
            "current_likes": None,
            "current_views": None,
            "popularity_rating": None,
            "date": None,
            "sentiment_rating": None,
            "tags": []
        }

    finally:
        if conn:
            cur.close()
            conn.close()

def get_id_by_date(search_date):
    try:
        conn = create_connection()
        cur = conn.cursor()

        if isinstance(search_date, str):
            search_date = datetime.strptime(search_date, "%Y-%m-%d").date()

        query = """
        SELECT id FROM date WHERE date = %s;
        """
        cur.execute(query, (search_date,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Error in db_reader.get_id_by_date: {e}")
        return None

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()