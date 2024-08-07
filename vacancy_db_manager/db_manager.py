import psycopg2
from prettytable import PrettyTable
from typing import Dict, Optional
from config import logger


class DBManager:
    def __init__(self, config: Dict[str, str]) -> None:
        """
        Initializes the DBManager with the provided configuration.
        Args:
            config (Dict[str, str]): Database configuration parameters.
        """
        self.config = config

    def __enter__(self) -> 'DBManager':
        """
        Opens a connection to the database and returns the DBManager instance.
        Returns:
            DBManager: The instance of the DBManager.
        """
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Exception]) -> None:
        """
        Closes the database connection and cursor.
        Args:
            exc_type (Optional[type]): The exception type.
            exc_val (Optional[Exception]): The exception value.
            exc_tb (Optional[Exception]): The traceback of the exception.
        """
        if exc_type is not None:
            logger.error(f'Произошла ошибка {exc_type} {exc_val}')
        self.cursor.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> PrettyTable:
        """
        Retrieves a list of all companies and the number of vacancies each company has.
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

    def get_all_vacancies(self) -> PrettyTable:
        """
        Retrieves a list of all vacancies with the company name, vacancy name, salary, and vacancy URL.
        Returns:
            PrettyTable: A formatted table containing the company name, vacancy name, salary, and URL.
        """
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
            table.field_names = ["Компания", "Вакансия", "Зарплата", "Ссылка на вакансию"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий: {e}")
            raise

    def get_avg_salary(self) -> PrettyTable:
        """
        Retrieves the average salary of all vacancies from the database.
        Returns:
            PrettyTable: A formatted table containing the average salary. The table has one column.
        """
        query = """
        SELECT ROUND(AVG(v.salary)) as avg_salary
        FROM vacancies v
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Средняя зарплата"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при получении средней зарплаты: {e}")
            raise

    def get_vacancies_with_higher_salary(self) -> PrettyTable:
        """
        Retrieves a list of all vacancies with a salary higher than the average salary of all vacancies.
        Returns:
            PrettyTable: A formatted table containing the company name, vacancy name, salary, and URL.
        """
        query = """
        WITH avg_salary AS (
            SELECT AVG(salary) AS average_salary
            FROM vacancies
        )
        SELECT e.employer_name, v.name, v.salary, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        CROSS JOIN avg_salary
        WHERE v.salary > avg_salary.average_salary;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Компания", "Вакансия", "Зарплата", "Ссылка на вакансию"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            raise

    def get_vacancies_with_keyword(self, keyword: str) -> PrettyTable:
        """
        Retrieves a list of all vacancies where the job title or description contains the specified keyword.
        Args:
            keyword (str): The keyword to search for in the job titles and descriptions.
        Returns:
            PrettyTable: A formatted table containing the job title, salary, and URL of each matching
                         vacancy.
        """
        query = """
        SELECT name, salary, url
        FROM vacancies
        WHERE name ILIKE %s OR description ILIKE %s
        """
        params = (f'%{keyword}%', f'%{keyword}%')

        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Название вакансии", "Зарплата", "Ссылка"]

            for row in result:
                table.add_row(row)

            return table
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий с ключевым словом '{keyword}': {e}")
            raise
