from pydantic import BaseModel


class SoftwareEngineer(BaseModel):
    main_language: str
    years_experience: float
    likes_coffee: bool
    password: str
