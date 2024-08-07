import requests
import jmespath
from typing import List

from vacancy_db_manager.models import Employer, Vacancy


BASE_URL_EMPLOYERS = "https://api.hh.ru/employers"
BASE_URL_VACANCIES = "https://api.hh.ru/vacancies"
EMPLOYERS_ID = [9694561, 4219, 5919632, 5667343, 9301808,
                6062708, 4306, 1740, 78638, 3529,
                2748, 1057, 2180, 87021, 15478, 84585, 3776]


def get_employers() -> List[Employer]:
    """
    Fetches employer details from a list of employer IDs.
    This function iterates through a predefined list of employer IDs, makes a GET request to fetch details
    for each employer, and extracts specific fields using a JMESPath query. The extracted data is then used
    to create instances of the Employer model which are collected into a list and returned.
    Returns:
        List[Employer]: A list of Employer objects containing details about each employer.
    """
    employers_data = []
    for company_id in EMPLOYERS_ID:
        url = f'{BASE_URL_EMPLOYERS}/{company_id}'
        response = requests.get(url=url)
        if response.status_code == 200:
            query = """
            {
                employer_id: id,
                employer_name: name,
                url: alternate_url
            }
            """
            parsed_data = jmespath.search(query, response.json())
            employers_data.append(Employer(**parsed_data))
    return employers_data


def get_vacancies(id: str) -> List[Vacancy]:
    """
    Fetches vacancy details for a specific employer ID.
    This function makes a GET request to fetch vacancies for a given employer ID, extracts specific fields
    from each vacancy using a JMESPath query, and creates instances of the Vacancy model. These instances
    are collected into a list and returned.
    Args:
        id (str): The ID of the employer whose vacancies are to be fetched.
    Returns:
        List[Vacancy]: A list of Vacancy objects containing details about each vacancy.
    """
    vacancies_data = []
    url = f'{BASE_URL_VACANCIES}?employer_id={id}&per_page=50&professional_role=96'
    response = requests.get(url=url)
    if response.status_code == 200:
        vacancies = response.json()['items']
        for vac in vacancies:
            query = """
            {
                vacancy_id: id,
                employer_id: employer.id,
                name: name,
                description: snippet.requirement || '' && snippet.responsibility || '',
                salary: salary.from,
                url: alternate_url
            }
            """
            parsed_data = jmespath.search(query, vac)
            vacancies_data.append(Vacancy(**parsed_data))
    return vacancies_data


def get_all_vacancies() -> List[Vacancy]:
    """
    Fetches all vacancies for a predefined list of employer IDs.
    This function iterates through a predefined list of employer IDs, fetches vacancies for each employer using
    the get_vacancies function, and aggregates all vacancies into a single list which is then returned.
    Returns:
        List[Vacancy]: A list of all Vacancy objects from all employers.
    """
    vacancies_data = []
    for company_id in EMPLOYERS_ID:
        vacancies = get_vacancies(company_id)
        vacancies_data.extend(vacancies)
    return vacancies_data
