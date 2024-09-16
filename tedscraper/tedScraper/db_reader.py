import psycopg2
from db_conn import create_connection

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

def get_video_statistic(video_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        query = f"""
        SELECT current_likes, historic_likes, current_views, historic_views FROM statistic WHERE video_id = '{video_id}'
        """
        cur.execute(query)
        data = cur.fetchall()

        columns = ['current_likes', 'historic_likes', 'current_views', 'historic_views']
        data_dict = dict(zip(columns, data[0]))
        return data_dict
    except:
        print(f"geen statistieken voor video met id: {video_id} gevonden")
        return {
            "current_likes" : None,
            "historic_likes": None,
            "current_views": None,
            "historic_views": None
        }