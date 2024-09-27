import allure
import requests
import variables
import pytest


class TestListOrder:
    @allure.title("Получение списка заказов")
    @allure.step("Отправка GET для получения списка заказов")
    def test_list_order_success(self):
        response = requests.get(variables.ApiUrls.BASE_ORDER_URL)

        assert response.status_code == 200, f'Статус код {response.status_code}'
        assert "orders" in response.json(), f'Нет ключа orders'
        assert len(response.json()["orders"]) > 0, f'Список пустой'
