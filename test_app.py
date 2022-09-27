import asyncio
from tortoise_models import SoftwareEngineers
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from main import app

from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["tortoise_models"])
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_dynamic_routing():
    client = TestClient(app)
    number: int = 10
    response = client.get(f"/dynamic_routing/{number}")
    assert response.status_code == 200
    assert response.json() == {"number": number}


def test_dynamic_routing_with_query_params():
    client = TestClient(app)
    number: int = 10
    add: int = 12
    multiply: int = 4
    response = client.get(
        f"/dynamic_routing/{number}", params={"add": add, "multiply": multiply}
    )
    assert response.status_code == 200
    assert response.json() == {"number": (number + add) * multiply}


def test_create_engineer():
    client = TestClient(app)
    main_language: str = "Python"
    years_experience: int = 2
    likes_coffee: bool = True
    password: str = "my_super_secret_password"

    payload = {
        "main_language": main_language,
        "years_experience": years_experience,
        "likes_coffee": likes_coffee,
        "password": password,
    }

    response = client.post("/software_engineers/", json=payload)
    assert response.status_code == 200
    assert response.json() != payload
    assert "password" not in response.json().keys()


def test_create_engineer(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    main_language: str = "Python"
    years_experience: int = 2
    likes_coffee: bool = True
    password: str = "mysupersecretpassword"

    payload = {
        "main_language": main_language,
        "years_experience": years_experience,
        "loves_coffee": likes_coffee,
        "password": password,
    }

    response = client.post("/software_engineers/", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert "password_hash" not in data.keys()

    async def get_engineer_by_db():
        engineer = await SoftwareEngineers.get(uuid=data.get("uuid"))
        return engineer

    eng_obj = event_loop.run_until_complete(get_engineer_by_db())

    assert str(eng_obj.uuid) == data.get("uuid")
