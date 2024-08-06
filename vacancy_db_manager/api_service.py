import requests
from typing import List


BASE_URL = "https://api.hh.ru/employers"


def get_employers() -> List[dict]:
    """
    Fetch a list of IT employers with open vacancies from the HeadHunter API.

    This function sends a GET request to the HeadHunter API to retrieve a list of employers
    who have open vacancies in the IT sector. The function sorts the results by the number
    of open vacancies and limits the number of results to 10. The locale for the search is set to "RU".

    Returns:
        List[dict]: A list of dictionaries where each dictionary represents an employer
                    with details such as id, name, alternate_url, and open_vacancies.
                    Returns an empty list if the request fails.
    """
    params = {
        "text": 'IT',
        "only_with_vacancies": True,
        "sort_by": "by_vacancies_open",
        "per_page": 10,
        "locale": "RU"
    }

    response = requests.get(url=BASE_URL, params=params)

    if response.status_code == 200:
        employers_data = response.json()["items"]
        return employers_data
    else:
        print(f"Ошибка получения работодателей: {response.status_code}")
        return []
