import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT')
}

MASTER_DATABASE_CONFIG = {
    'dbname': 'postgres',
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT')
}

CREATE_TABLES_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS employers (
        id SERIAL PRIMARY KEY,
        employer_id INTEGER NOT NULL UNIQUE,
        employer_name VARCHAR(100) NOT NULL,
        url TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id INTEGER NOT NULL,
        employer_id INTEGER NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        salary INTEGER,
        url TEXT NOT NULL,
        FOREIGN KEY (employer_id) REFERENCES employers (employer_id) ON DELETE CASCADE
    );
    """
]


def create_database_if_not_exists(dbname: str):
    """
    Connects to the PostgreSQL server and creates the database if it does not exist.
    Args:
        dbname (str): The name of the database to create.
    """
    conn = psycopg2.connect(**MASTER_DATABASE_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;"), [dbname])
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"База данных'{dbname}' успешно создана")
        else:
            print(f"База данных '{dbname}' уже существует")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cursor.close()
        conn.close()


def create_tables():
    """
    Connects to the PostgreSQL database and creates the employers and vacancies tables.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    try:
        for query in CREATE_TABLES_QUERIES:
            cursor.execute(query)
        conn.commit()
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()