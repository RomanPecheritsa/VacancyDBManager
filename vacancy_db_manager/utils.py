from typing import List

from vacancy_db_manager.models import Employer


def json_to_data_employers(employers_data) -> List[Employer]:
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
