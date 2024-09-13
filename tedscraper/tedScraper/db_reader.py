import psycopg2
from db_conn import create_connection

def get_video_ids():
    conn = create_connection()
    cur = conn.cursor()
    query = """
    SELECT video_id FROM video_data;
    """
    cur.execute(query)
    dirty_ids = cur.fetchall()  # List van tuples [(id1,), (id2,), ...]
    clean_ids = []

    # Unpack de tuples en voeg de schoongemaakte video_id toe aan de lijst
    for (video_id,) in dirty_ids:
        clean_ids.append(clean_video_id(video_id))

    return clean_ids

def clean_video_id(video_id):
    return video_id.strip("',()")