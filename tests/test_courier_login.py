import allure
import requests
import variables
import pytest

from conftest import create_courier


# @pytest.fixture
# def create_courier_fixture():
#     return create_courier()


class TestCourierLogin:
    @allure.title("Успешний логин")
    @allure.step("Отправка POST для проверки умпешного логина")
    def test_courier_login_success(self, create_courier):
        login_pass = create_courier
        login = login_pass[0]
        password = login_pass[1]
        response = requests.post(variables.ApiUrls.COURIER_LOGIN_URL, json={"login": login, "password": password})

        assert response.status_code == 200, f'Статус код {response.status_code}'
        assert response.json()["id"] is not None, f'Тело {response.json()["id"]}'

    @allure.title("Логин без пароля")
    @allure.step("Отправка POST для проверки логина без пароля")
    def test_courier_login_miss(self, create_courier):
        login = create_courier[0]
        payload = {
            "login": login
        }
        response = requests.post(variables.ApiUrls.COURIER_LOGIN_URL, json=payload)

        assert response.status_code == 504, f'Статус код {response.status_code}'

    @allure.title("Логин без логина")
    @allure.step("Отправка POST для проверки логина без логина")
    def test_courier_password_miss(self, create_courier):
        password = create_courier[1]
        payload = {
            "password": password
        }
        response = requests.post(variables.ApiUrls.COURIER_LOGIN_URL, json=payload)

        assert response.status_code == 400, f'Статус код {response.status_code}'
        assert response.json()["message"] == "Недостаточно данных для входа", f'Тело {response.json()["message"]}'

    @allure.title("Логин с неправильным параметрам")
    @allure.step("Отправка POST для проверки логина неправильным параметром")
    def test_courier_invalid_filed(self, create_courier):
        login_pass = create_courier
        login = login_pass[0]
        password = login_pass[1].swapcase()

        response = requests.post(variables.ApiUrls.COURIER_LOGIN_URL, json={"login": login, "password": password})

        assert response.status_code == 404, f'Статус код {response.status_code}'
        assert response.json()["message"] == "Учетная запись не найдена", f'Тело {response.json()["message"]}'

    @allure.title("Логин с несуществующем пользователем")
    @allure.step("Отправка POST для проверки несуществующем пользователем")
    def test_courier_authorized_duplicate(self, create_courier):
        login_pass = create_courier
        login = login_pass[0].swapcase()
        password = login_pass[1]

        response = requests.post(variables.ApiUrls.COURIER_LOGIN_URL, json={"login": login, "password": password})

        assert response.status_code == 404, f'Статус код {response.status_code}'
        assert response.json()["message"] == "Учетная запись не найдена", f'Тело {response.json()["message"]}'
