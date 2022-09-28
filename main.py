from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import argon2
import uvicorn

from models import SoftwareEngineer
from tortoise_models import SoftwareEngineer_Pydantic, SoftwareEngineerIn, SoftwareEngineers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/dynamic_routing/{number}")
async def return_number(number: int, add: int = 0, multiply: int = 1):
    return {"number": (number + add) * multiply}


@app.post(
    "/software_engineers_old/",
    response_model=SoftwareEngineer,
    response_model_exclude=["password"],
)
async def new_engineer(engineer: SoftwareEngineer):
    return engineer

@app.post(
    "/software_engineers/",
    response_model=SoftwareEngineer_Pydantic,
    response_model_exclude=["password_hash"],
)
async def new_engineer(engineer: SoftwareEngineerIn):
    # password_hash = argon2.hash_password_raw(engineer.password, "some_salt")
    password_hash = "123"
    engineer_dict = engineer.dict()
    engineer_dict.update({"password_hash": password_hash})
    engineer_dict.pop("password")
    software_eng_obj = await SoftwareEngineers.create(**engineer_dict)
    return await SoftwareEngineer_Pydantic.from_tortoise_orm(software_eng_obj)

register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["tortoise_models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7040, log_level="debug")
