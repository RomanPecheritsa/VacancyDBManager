from pydantic import BaseModel


class Employer(BaseModel):
    id: str
    name: str
    open_vacancies: int
