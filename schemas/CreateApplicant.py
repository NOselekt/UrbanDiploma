from pydantic import BaseModel


class CreateApplicant(BaseModel):
    '''
    Pydantic model for getting applicant model from HTML form.
    '''

    snils: int
    score: int = 0
    olimp: bool = False
    password: str
    courses: list[str]
