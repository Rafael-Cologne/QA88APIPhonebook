

class TestLogin:

    def test_login_positive(self, session, login_url, registered_user):
        body = {
            "username": registered_user.username,
            "password": registered_user.password,
        }
        headers = {"Content-Type": "application/json"}
        response = session.post(login_url, json=body, headers=headers)
        assert response.status_code == 200
        assert "token" in response.json().keys()

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