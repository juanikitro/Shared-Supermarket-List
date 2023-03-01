from django.test import TestCase
from .models import Product
from http.cookies import SimpleCookie
from simple_users.models import SimpleUser


PRODUCTS_ENDPOINT = "/api/products/"


class ProductsEndpointsTests(TestCase):
    def setUp(self):  # Login
        return SimpleUser.objects.get_or_create({"username": "PanchitoTesting"})

    def test_create_product(self):
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.post(
            PRODUCTS_ENDPOINT, {"name": "testing product", "owner": 1, "priority": 3, "quantity": 4, "price": 100}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "testing product",
                "owner": 1,
                "priority": 3,
                "quantity": 4,
                "price": "100.00",
                "total": 400.0,
            },
        )
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().id, 1)
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.post(
            PRODUCTS_ENDPOINT,
            {
                "name": "second testing",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["priority"], 1)
        self.assertEqual(response.data["quantity"], 1)
        self.assertEqual(response.data["price"], "0.00")
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().id, 2)

    def test_list_products(self):
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.get(PRODUCTS_ENDPOINT)
        self.assertEqual(response.data, [])

        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        self.client.post(PRODUCTS_ENDPOINT, {"name": "listtest", "owner": 1})

        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.get(PRODUCTS_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        print("anashe")
        print(response.json())
        self.assertEqual(
            response.json(),
            [
                {
                    "id": 1,
                    "name": "listtest",
                    "priority": 1,
                    "quantity": 1,
                    "price": "0.00",
                    "total": 0.0,
                    "owner": 1,
                    "group": None,
                }
            ],
        )
        self.assertEqual(len(response.json()), 1)

    def test_product_detail(self):
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.get(f"{PRODUCTS_ENDPOINT}1/")
        self.assertEqual(response.status_code, 404)

        self.client.post(PRODUCTS_ENDPOINT, {"name": "retrieve test", "owner": 1})
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.get(f"{PRODUCTS_ENDPOINT}1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "retrieve test", "owner": 1, "priority": 1, "quantity": 1, "price": "0.00", "total": 0.0},
        )

    def test_product_update(self):
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        self.client.post(PRODUCTS_ENDPOINT, {"name": "test", "owner": 1})
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.put(
            f"{PRODUCTS_ENDPOINT}1/update/", {"name": "updatedname", "price": 10}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["name"],
            "updatedname",
        )
        self.assertEqual(
            response.json()["price"],
            "10.00",
        )

    def test_product_delete(self):
        self.client.post(PRODUCTS_ENDPOINT, {"name": "test"})
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.delete(f"{PRODUCTS_ENDPOINT}1/delete/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)
        self.client.cookies = SimpleCookie({"sessionid": "PanchitoTesting"})
        response = self.client.get(f"{PRODUCTS_ENDPOINT}1/")
        self.assertEqual(response.status_code, 404)
