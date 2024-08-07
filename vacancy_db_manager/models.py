from pydantic import BaseModel
from typing import Optional


class Employer(BaseModel):
    """
    Model representing an employer.
    Attributes:
        employer_id (str): The unique identifier of the employer.
        employer_name (str): The name of the employer.
        url (str): The URL link to the employer's profile or webpage.
    """
    employer_id: int
    employer_name: str
    url: str


class Vacancy(BaseModel):
    """
    Model representing a vacancy.
    Attributes:
        vacancy_id (str): The unique identifier of the vacancy.
        employer_id (str): The unique identifier of the employer who posted the vacancy.
        name (str): The name or title of the vacancy.
        description (Optional[str]): The description or requirements of the vacancy. Defaults to None.
        salary (Optional[int]): The offered salary for the vacancy. Defaults to None.
        url (str): The URL link to the vacancy's detailed webpage.
    """
    vacancy_id: int
    employer_id: int
    name: str
    description: Optional[str] = None
    salary: Optional[int] = None
    url: str
