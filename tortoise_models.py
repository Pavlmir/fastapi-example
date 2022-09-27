from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class SoftwareEngineers(Model):
    uuid = fields.UUIDField(pk=True)
    loves_coffee = fields.BooleanField(default=True)
    years_experience = fields.FloatField()
    main_language = fields.CharField(max_length=128)
    password_hash = fields.CharField(max_length=500)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now_add=True)


SoftwareEngineer_Pydantic = pydantic_model_creator(
    SoftwareEngineers, name="SoftwareEngineer"
)


class SoftwareEngineerIn(BaseModel):
    loves_coffee: bool
    years_experience: float
    password: str
    main_language: str
