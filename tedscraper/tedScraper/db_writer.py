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
    CREATE TABLE IF NOT EXISTS video_statistics (
    video_id VARCHAR(255) NOT NULL,
    record_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    views INT NOT NULL,
    likes INT NOT NULL,
    captions VARCHAR,  -- Optioneel: je kunt een lengte specificeren, zoals VARCHAR(500)
    PRIMARY KEY (video_id)
);
    """
    cur.execute(query)
    conn.commit()
    cur.close()

def insert_video_into_db(statistics):
    conn = psycopg2.connect(
        database="dataadvanced",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    insert_query = """
        INSERT INTO video_statistics (video_id, record_date, views, likes)
        VALUES (%s, CURRENT_TIMESTAMP, %s, %s)
        ON CONFLICT (video_id) DO NOTHING;
        """

    try:
        # Voer de query uit met data uit de video_metadata dictionary
        cur.execute(insert_query, (
            statistics["video_id"],
            statistics["views"],
            statistics["likes"]
        ))

        # Sla de veranderingen op in de database
        conn.commit()

        print("Video metadata succesvol ingevoegd.")
    except Exception as e:
        # Rollback bij fouten
        conn.rollback()
        print(f"Fout bij het invoegen van video metadata: {e}")
    finally:
        # Sluit de cursor
        cur.close()