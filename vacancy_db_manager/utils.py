from typing import List

from vacancy_db_manager.models import Employer


def json_to_data_employers(employers_data: List[dict]) -> List[Employer]:
    """
    Converts a list of dictionaries with employer data into a list of objects of the Employer model.

    This function accepts a list of dictionaries, where each dictionary contains information about the employer,
    and creates objects of the Employer model from them by unpacking values from the dictionary.
    Args:
        employers_data (List[dict]): A list of dictionaries,
        where each dictionary contains information about the employer.
    Returns:
        List[Employer]: A list of objects of the Employer model created based on the input data.
    """
    return [Employer(**item) for item in employers_data]


def get_employers_ids(data_employers: List[Employer]) -> List[str]:
    """
    Extracts the IDs of employers from a list of Employer objects.
    This function takes a list of Employer instances and returns a list containing
    the IDs of these employers. It is useful for retrieving the unique identifiers
    of employers for further processing or querying.
    Args:
        data_employers (List[Employer]): A list of Employer objects from which the IDs
                                         are to be extracted.
    Returns:
        List[str]: A list of strings, each representing an employer ID. If the input
                   list is empty, an empty list is returned.
    """
    return [item.id for item in data_employers]
