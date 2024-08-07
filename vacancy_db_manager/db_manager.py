import psycopg2
from psycopg2 import sql
from prettytable import PrettyTable
from config import logger


class DBManager:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(f'Произошла ошибка {exc_type} {exc_val}')
        self.cursor.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Gets a list of all companies and the number of vacancies each company has.
        Returns:
            PrettyTable: A formatted table containing the company name and the count of vacancies.
        """
        query = """
        SELECT e.employer_name, COUNT(v.vacancy_id) as vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        GROUP BY e.employer_name
        ORDER BY vacancies_count DESC;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Компания", "Количество вакансий"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при поиске компаний и подсчете вакансий: {e}")
            raise

    def get_all_vacancies(self):
        query = """
        SELECT e.employer_name, v.name, v.salary, v.url
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        ORDER BY v.salary DESC;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Компания", "Вакансия", "Зарплата", "Ссылка на ваканисю"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий: {e}")
            raise

