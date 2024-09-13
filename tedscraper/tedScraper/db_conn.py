import psycopg2

def create_connection():
    conn = psycopg2.connect(
        database="dataadvanced",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )

    return conn
