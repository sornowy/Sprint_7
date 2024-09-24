import allure
import requests
import variables
import pytest
from test_data import get_order_payload


class TestOrderCreate:
    @allure.title("Создание заказа с разными цветами")
    @allure.step("Отправка POST для проверки создания заказа с разными цветами, цвета в color_option")
    @pytest.mark.parametrize("color_option", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_order_create_success(self, color_option):
        payload = get_order_payload(color_option)
        response = requests.post(variables.BASE_ORDER_URL, json=payload)

        assert response.status_code == 201, f'Статус код {response.status_code}'
        assert response.json()["track"] is not None, f'Тело {response.json()["track"]}'
