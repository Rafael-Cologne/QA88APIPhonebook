import pytest
import requests
import random
import time
from config import *
from faker import Faker

from models.user_dto import User

fake = Faker()


@pytest.fixture(scope="session")
def registration_url():
    return BASE_URL + API_VERSION + REGISTRATION_URL

@pytest.fixture(scope="session")
def login_url():
    return BASE_URL + API_VERSION + LOGIN_URL


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture(scope="function")
def random_user():
    username = f"qa_{int(time.time())}_{fake.email()}"
    password = fake.password(
        length=random.randint(8, 15),
        special_chars=False,
        digits=True,
        upper_case=True,
        lower_case=True,
    )+"$"
    return User(username=username, password=password)

@pytest.fixture(scope="function")
def registered_user(session, registration_url, random_user):
    user_data = {
        "username": random_user.username,
        "password": random_user.password,
    }
    response_reg = session.post(registration_url, json=user_data)
    if response_reg.status_code == 200:
        return random_user
    return User(TEST_EMAIL, TEST_PASSWORD)