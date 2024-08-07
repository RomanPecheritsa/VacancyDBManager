import os
from vacancy_db_manager.api_service import get_employers, get_all_vacancies
from vacancy_db_manager.db_creator import (create_database, create_tables,
                                           insert_employers, insert_vacancies)
from vacancy_db_manager.db_manager import DBManager
from config import DATABASE_CONFIG


def main_user_menu() -> None:
    """
    The main function for user interaction
    """
    input('Добро пожаловать!\nНажмите Enter для начала работы\n')

    print('Получение вакансий из API hh.ru. Пожалуйста подождите ...\n')
    employers_data = get_employers()
    vacancies_data = get_all_vacancies()
    print(f'Получено {len(vacancies_data)} вакансий от {len(employers_data)} работадателей\n')

    print('Создание и наполнение базы данных ...\n')
    create_database(os.getenv('DATABASE_NAME'))
    create_tables()
    insert_employers(employers_data)
    insert_vacancies(vacancies_data)
    print()

    while True:
        print('\n1. Получить список всех компаний и количество вакансий у каждой компании')
        print('2. Получить список всех вакансий с указанием компании, вакансии, зарплаты и ссылки на вакансию')
        print('3. Получить среднюю зарплату по вакансиям')
        print('4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям')
        print('5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова')
        print('6. Выход')

        user_choice = input('Выберите пункт меню: \n')
        print()

        if user_choice == '1':
            menu_get_all_emp_count_vac()
        elif user_choice == '2':
            pass
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            pass
        elif user_choice == '5':
            pass
        elif user_choice == '6':
            print("\nВыход из программы\n")
            break
        else:
            print('\nНекорректный выбор, попробуйте еще раз\n')


def menu_get_all_emp_count_vac() -> None:
    """
    A function for interacting with the user when selecting
        'Получить список всех компаний и количество вакансий у каждой компании'
    """
    with DBManager(DATABASE_CONFIG) as db_manager:
        companies_vacancies_table = db_manager.get_companies_and_vacancies_count()
        if companies_vacancies_table:
            print(companies_vacancies_table)
        else:
            print("\nНет данных для отображения.")

