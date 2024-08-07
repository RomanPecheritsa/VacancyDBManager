import requests
import jmespath
from typing import List, Dict, Any

BASE_URL_EMPLOYERS = "https://api.hh.ru/employers"
BASE_URL_VACANCIES = "https://api.hh.ru/vacancies"
EMPLOYERS_ID = [1429999, 1035394, 3961360, 10772647, 84585, 5600787, 2180, 12550, 3529, 9498120]


def get_employers() -> List[Dict[str, Any]]:
    """
    Fetches details for a list of predefined employers.
    This function iterates through a predefined list of employer IDs, makes GET requests to fetch details
    for each employer, and extracts specific fields using a JMESPath query. The extracted data is collected
    into a list of dictionaries and returned.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing details about each employer. Each dictionary
                              includes 'employer_id', 'employer_name', and 'url'.
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


def get_vacancies(company_id: int) -> List[Dict[str, Any]]:
    """
    Fetches vacancy details for a specific employer.

    This function makes a GET request to fetch vacancies for a given employer ID. It extracts specific fields
    from each vacancy using a JMESPath query, calculates the salary if 'from' and 'to' are present, and returns
    a list of dictionaries containing details about each vacancy.
    Args:
        company_id (int): The ID of the employer whose vacancies are to be fetched.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing details about each vacancy. Each dictionary
                              includes 'vacancy_id', 'employer_id', 'name', 'description', 'salary', and 'url'.
    """
    vacancies_data = []
    url = f'{BASE_URL_VACANCIES}?employer_id={company_id}&per_page=100&only_with_salary=true'
    response = requests.get(url=url)
    if response.status_code == 200:
        vacancies = response.json().get('items', [])
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


def get_all_vacancies() -> List[Dict[str, Any]]:
    """
    Fetches all vacancies for a predefined list of employer IDs.
    This function iterates through a predefined list of employer IDs, fetches vacancies for each employer using
    the `get_vacancies` function, and aggregates all vacancies into a single list.
    Returns:
        List[Dict[str, Any]]: A list of all vacancies from all employers. Each dictionary includes 'vacancy_id',
                              'employer_id', 'name', 'description', 'salary', and 'url'.
    """
    vacancies_data = []
    for company_id in EMPLOYERS_ID:
        vacancies = get_vacancies(company_id)
        vacancies_data.extend(vacancies)
    return vacancies_data
