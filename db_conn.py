import psycopg2
import os
from dotenv import load_dotenv


def create_connection():
    load_dotenv()
    conn = psycopg2.connect(
        database=os.environ['DATABASE_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )

    return conn
