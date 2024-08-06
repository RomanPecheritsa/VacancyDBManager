import requests
from typing import List


BASE_URL = "https://api.hh.ru/employers"


def get_employers() -> List:
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
