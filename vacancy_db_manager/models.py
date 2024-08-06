from pydantic import BaseModel


class Employer(BaseModel):
    """
    Represents an employer with basic details such as ID, name, and the number of open vacancies.
    Attributes:
        id (str): The unique identifier for the employer.
        name (str): The name of the employer.
        open_vacancies (int): The number of open vacancies the employer currently has.
    """
    id: str
    name: str
    open_vacancies: int
