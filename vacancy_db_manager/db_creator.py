import psycopg2
from psycopg2 import sql
from config import DATABASE_CONFIG, MASTER_DATABASE_CONFIG, logger
from typing import List, Dict, Optional, Any

CREATE_TABLES_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS employers (
        employer_id INTEGER PRIMARY KEY,
        employer_name VARCHAR(250) NOT NULL,
        url TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id INTEGER NOT NULL UNIQUE,
        employer_id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        salary INTEGER,
        url TEXT NOT NULL,
        FOREIGN KEY (employer_id) REFERENCES employers (employer_id) ON DELETE CASCADE
    );
    """
]


def create_database(dbname: str) -> None:
    """
    Connects to the PostgreSQL server and creates a new database, dropping it first if it exists.
    Args:
        dbname (str): The name of the database to create.
    Returns:
        None
    """
    conn = psycopg2.connect(**MASTER_DATABASE_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(dbname)))
        print(f"База данных '{dbname}' удалена")

        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"База данных '{dbname}' успешно создана")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")
    finally:
        cursor.close()
        conn.close()


def create_tables() -> None:
    """
    Connects to the PostgreSQL database and creates the employers and vacancies tables if they do not exist.
    Returns:
        None
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    try:
        for query in CREATE_TABLES_QUERIES:
            cursor.execute(query)
        conn.commit()
        print("Таблицы успешно созданы")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_employers(employers: List[Dict[str, Optional[str]]]) -> None:
    """
    Inserts employers into the database.
    Args:
        employers (List[Dict[str, Optional[str]]]): A list of dictionaries where each dictionary contains
                                                   'employer_id', 'employer_name', and 'url' for an employer.
    Returns:
        None
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    try:
        for emp in employers:
            cursor.execute(
                sql.SQL("INSERT INTO employers (employer_id, employer_name, url) "
                        "VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING;"),
                (emp['employer_id'], emp['employer_name'], emp['url'])
            )
        conn.commit()
        print("Данные о работодателях успешно вставлены")
    except Exception as e:
        logger.error(f"Ошибка при вставке данных о работодателях: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_vacancies(vacancies: List[Dict[str, Optional[Any]]]) -> None:
    """
    Inserts vacancies into the database.
    Args:
        vacancies (List[Dict[str, Optional[Any]]]): A list of dictionaries where each dictionary contains
                                                   'vacancy_id', 'employer_id', 'name', 'description',
                                                   'salary', and 'url' for a vacancy.
    Returns:
        None
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    try:
        for vac in vacancies:
            cursor.execute(
                sql.SQL(
                    "INSERT INTO vacancies (vacancy_id, employer_id, name, description, salary, url) "
                    "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING;"),
                (vac['vacancy_id'], vac['employer_id'], vac['name'], vac.get('description'), vac.get('salary'),
                 vac['url'])
            )
        conn.commit()
        print("Данные о вакансиях успешно вставлены")
    except Exception as e:
        logger.error(f"Ошибка при вставке данных о вакансиях: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
