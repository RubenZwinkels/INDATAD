import psycopg2

def create_table():
    conn = psycopg2.connect(
        database = "dataadvanced",
        user = "postgres",
        password = "postgres",
        host = "localhost",
        port = 5432
    )
    cur = conn.cursor()

    query = """
     CREATE TABLE IF NOT EXISTS  (
             video_id SERIAL PRIMARY KEY,
             data_column TEXT NOT NULL,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             );
    """
    cur.execute(query)
    conn.commit()
    cur.close()