import allure
import requests
import variables
import pytest
from test_data import generate_courier_data


class TestCourierCreate:
    @allure.title("Успешное создание курьера")
    @allure.step("Отправка POST для проверки создания курьера")
    def test_courier_success(self):
        courier_data = generate_courier_data()
        response = requests.post(variables.COURIER_BASE_URL, json=courier_data)

        assert response.status_code == 201, f'Статус код {response.status_code}'
        assert response.json()["ok"] is True, f'Тело {response.json()["ok"]}'

    @allure.title("Создание дупликата курьера")
    @allure.step("Отправка POST для проверки создания 2 одиноковых курьеров")
    def test_courier_duplicat(self):
        courier_data = generate_courier_data()
        response_1 = requests.post(variables.COURIER_BASE_URL, json=courier_data)

        assert response_1.status_code == 201, f'Статус код {response_1.status_code}'
        assert response_1.json()["ok"] is True, f'Тело {response_1.json()["ok"]}'

        response_2 = requests.post(variables.COURIER_BASE_URL, json=courier_data)

        assert response_2.status_code == 409, f'Статус код {response_2.status_code}'
        assert response_2.json()["message"] == "Этот логин уже используется. Попробуйте другой.", f'Тело {response_2.json()["message"]}'

    @allure.title("Создать курьера без обязательных полей")
    @allure.step("Отправка POST для проверки создания курьера без обязательных полей")
    @pytest.mark.parametrize("miss_field", ["login", "password"])
    def test_courier_miss_field(self, miss_field):
        courier_data = generate_courier_data()
        courier_data.pop(miss_field, None)

        response = requests.post(variables.COURIER_BASE_URL, json=courier_data)

        assert response.status_code == 400, f'Статус код {response.status_code}'
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f'Тело {response.json()["message"]}'



