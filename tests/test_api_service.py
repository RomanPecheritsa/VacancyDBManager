import pytest
import requests
import requests_mock
from typing import List

from vacancy_db_manager.api_service import get_employers, BASE_URL


@pytest.fixture
def mock_employers_data():
    """
    Fixture to provide mock data for the list of employers.
    """
    return [
        {
            "id": "1",
            "name": "Company A",
            "alternate_url": "https://example.com/company_a",
            "open_vacancies": 5
        },
        {
            "id": "2",
            "name": "Company B",
            "alternate_url": "https://example.com/company_b",
            "open_vacancies": 10
        }
    ]


def test_get_employers_success(requests_mock, mock_employers_data):
    """
    Test that `get_employers` returns a list of employers when the API request is successful.
    Args:
        requests_mock (Mocker): The requests-mock fixture for mocking HTTP requests.
        mock_employers_data (List[dict]): Mock data for the list of employers.
    """
    params = {
        "text": 'IT',
        "only_with_vacancies": True,
        "sort_by": "by_vacancies_open",
        "per_page": 10,
        "locale": "RU"
    }

    employers_url = BASE_URL
    requests_mock.get(employers_url, json={"items": mock_employers_data}, status_code=200)

    employers = get_employers()
    assert len(employers) == 2
    assert employers[0]["id"] == "1"
    assert employers[0]["name"] == "Company A"
    assert employers[0]["alternate_url"] == "https://example.com/company_a"
    assert employers[0]["open_vacancies"] == 5


def test_get_employers_failure(requests_mock):
    """
    Test that `get_employers` returns an empty list when the API request fails.
    Args:
        requests_mock (Mocker): The requests-mock fixture for mocking HTTP requests.
    """
    employers_url = BASE_URL
    requests_mock.get(employers_url, status_code=500)

    employers = get_employers()
    assert employers == []
