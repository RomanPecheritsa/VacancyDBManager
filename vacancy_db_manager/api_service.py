import requests
import jmespath
from typing import List


BASE_URL_EMPLOYERS = "https://api.hh.ru/employers"
BASE_URL_VACANCIES = "https://api.hh.ru/vacancies"
EMPLOYERS_ID = [1429999, 1035394, 3961360, 10772647, 84585, 5600787, 2180, 12550, 3529, 9498120]


def get_employers() -> List[dict]:
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
            employers_data.append(parsed_data)
    return employers_data


def get_vacancies(company_id: int) -> List[dict]:
    """
    Fetches vacancy details for a specific employer ID.
    This function makes a GET request to fetch vacancies for a given employer ID, extracts specific fields
    from each vacancy using a JMESPath query, and creates instances of the Vacancy model. These instances
    are collected into a list and returned.
    Args:
        company_id (int): The ID of the employer whose vacancies are to be fetched.
    Returns:
        List[Vacancy]: A list of Vacancy objects containing details about each vacancy.
    """
    vacancies_data = []
    url = f'{BASE_URL_VACANCIES}?employer_id={company_id}&per_page=100&only_with_salary=true'
    response = requests.get(url=url)
    if response.status_code == 200:
        vacancies = response.json()['items']
        for vac in vacancies:
            salary_from = vac.get('salary', {}).get('from')
            salary_to = vac.get('salary', {}).get('to')
            salary = salary_from if salary_from is not None else salary_to

            query = """
            {
                vacancy_id: id,
                employer_id: employer.id,
                name: name,
                description: snippet.requirement || '' && snippet.responsibility || '',
                salary: salary,
                url: alternate_url
            }
            """
            parsed_data = jmespath.search(query, vac)
            parsed_data['salary'] = salary
            vacancies_data.append(parsed_data)
    return vacancies_data


def get_all_vacancies() -> List[dict]:
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
