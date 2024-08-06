import pytest
from typing import List
from vacancy_db_manager.models import Employer
from vacancy_db_manager.utils import json_to_data_employers, get_employers_ids


@pytest.fixture
def mock_employers_data():
    """
    Fixture to provide mock data for employer conversion.
    """
    return [
        {
            "id": "1",
            "name": "Company A",
            "open_vacancies": 5
        },
        {
            "id": "2",
            "name": "Company B",
            "open_vacancies": 10
        }
    ]


@pytest.fixture
def mock_employers():
    """
    Fixture to provide a list of Employer objects.
    """
    return [
        Employer(id="1", name="Company A", open_vacancies=5),
        Employer(id="2", name="Company B", open_vacancies=10)
    ]


def test_json_to_data_employers(mock_employers_data):
    """
    Test that `json_to_data_employers` correctly converts a list of dictionaries into a list of Employer objects.
    Args:
        mock_employers_data (List[dict]): Mock data containing a list of employer dictionaries.
    """
    employers = json_to_data_employers(mock_employers_data)

    assert len(employers) == 2
    assert employers[0].id == "1"
    assert employers[0].name == "Company A"
    assert employers[0].open_vacancies == 5
    assert employers[1].id == "2"
    assert employers[1].name == "Company B"
    assert employers[1].open_vacancies == 10


def test_get_employers_ids(mock_employers):
    """
    Test that `get_employers_ids` correctly extracts IDs from a list of Employer objects.
    Args:
        mock_employers (List[Employer]): Mock data containing a list of Employer objects.
    """
    ids = get_employers_ids(mock_employers)

    assert ids == ["1", "2"]
