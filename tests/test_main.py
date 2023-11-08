import requests
import pytest


URL = 'https://reqres.in/api/'


def pytest_addoption(parser):
    parser.addoption(
        "--slow",
        default="true",
        choices=("true", "false")
    )

pytest.fixture
def slow(request):
    return request.config.getoption("--slow")


@pytest.fixture
def number():
    number = {
        "2": 2,
        "3": 3,
        "23": 23
    }
    return number

@pytest.fixture
def user_data():
    user_data = {
        "name": "morpheus",
        "job": "leader"
    }
    return user_data

@pytest.fixture
def user_update_data():
    user_update_data = {
        "name": "morpheus",
        "job": "zion resident"
    }
    return user_update_data


@pytest.fixture
def register():
    register = [
        {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        },
        {
            "id": 4,
            "token": "QpwL5tke4Pnpja7X4"
        }
    ]
    return register

@pytest.fixture
def register_false():
    register_false = [
        {
            "email": "sydney@fife"
        },
        {
            "error": "Missing password"
        }
    ]
    return register_false

@pytest.fixture
def login():
    login = [
        {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        },
        {
            "token": "QpwL5tke4Pnpja7X4"
        }
    ]
    return login

@pytest.fixture
def login_false():
    login_false = [
        {
            "email": "peter@klaven"
        },
        {
            "error": "Missing password"
        }
    ]
    return login_false

class TestUsers:

    def test_api_number_page(self, number):
        route = f'{URL}' + 'users?page=' + f'{number["2"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 200
        assert result["page"] == 2

    def test_api_number_user(self, number):
        route = f'{URL}' + 'users/' f'{number["2"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 200
        assert result["data"]["id"] == 2

    def test_api_number_not_found_user(self, number):
        route = f'{URL}' + 'users/' f'{number["23"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 404
        assert result == {}

    def test_create_user(self, user_data):
        route = f'{URL}' + 'users/'
        response = requests.post(route, json=user_data)
        result = response.json()

        assert response.status_code == 201
        assert result["name"] == user_data["name"]
        assert result["job"] == user_data["job"]

    def test_put_user(self, user_update_data, number):
        route = f'{URL}' + 'users/' + f'{number["2"]}'
        response = requests.put(route, json=user_update_data)
        result = response.json()

        assert response.status_code == 200
        assert result["name"] == user_update_data["name"]
        assert result["job"] == user_update_data["job"]

    def test_patch_user(self, user_update_data, number):
        route = f'{URL}' + 'users/' + f'{number["2"]}'
        response = requests.patch(route, json=user_update_data)
        result = response.json()

        assert response.status_code == 200
        assert result["name"] == user_update_data["name"]
        assert result["job"] == user_update_data["job"]

    def test_delete_user(self, number):
        route = f'{URL}' + 'users/' + f'{number["2"]}'
        response = requests.delete(route)

        assert response.status_code == 204

    @pytest.mark.slow
    def test_api_number_page(self, number):
        route = f'{URL}' + 'users?delay=' + f'{number["3"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 200
        assert result["page"] == 1

class TestUnknown:
    def test_api_number_unknown_list(self):
        route = f'{URL}' + 'unknown'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 200
        assert result["page"] == 1

    def test_api_number_unknown_number(self, number):
        route = f'{URL}' + 'unknown/' +f'{number["2"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 200
        assert result["data"]["id"] == 2

    def test_api_number_not_found_unknown(self, number):
        route = f'{URL}' + 'unknown/' f'{number["23"]}'
        response = requests.get(route)
        result = response.json()

        assert response.status_code == 404
        assert result == {}


class TestRegister:
    def test_new_register(self, register):
        route = f'{URL}' + 'register'
        response = requests.post(route, json=register[0])
        result = response.json()

        assert response.status_code == 200
        assert result["id"] == register[1]["id"]
        assert result["token"] == register[1]["token"]
    
    def test_false_register(self, register_false):
        route = f'{URL}' + 'register'
        response = requests.post(route, json=register_false[0])
        result = response.json()

        assert response.status_code == 400
        assert result["error"] == register_false[1]["error"]


class TestLogin:
    def test_login(self, login):
        route = f'{URL}' + 'login'
        response = requests.post(route, json=login[0])
        result = response.json()

        assert response.status_code == 200
        assert result["token"] == login[1]["token"]
    
    def test_false_register(self, login_false):
        route = f'{URL}' + 'register'
        response = requests.post(route, json=login_false[0])
        result = response.json()

        assert response.status_code == 400
        assert result["error"] == login_false[1]["error"]