from django.test import TestCase
from .models import SimpleUser


USERS_ENDPOINT = "/api/users/"


class SimpleUserEndpointsTests(TestCase):
    def test_create_product(self):
        response = self.client.post(f"{USERS_ENDPOINT}register/", {"username": "Testing username"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {"id": 1, "username": "Testing username"},
        )
        self.assertEqual(SimpleUser.objects.count(), 1)
        self.assertEqual(SimpleUser.objects.first().id, 1)

        response = self.client.post(
            f"{USERS_ENDPOINT}register/",
            {
                "username": "Carlitos",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SimpleUser.objects.count(), 2)
        self.assertEqual(SimpleUser.objects.last().id, 2)

    def test_login_simulation(self):
        response = self.client.post(f"{USERS_ENDPOINT}login/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"error": "You must provide a username"})

        response = self.client.post(f"{USERS_ENDPOINT}login/", {"username": "Pancho"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"error": "Username Pancho does not exist"})

        self.client.post(f"{USERS_ENDPOINT}register/", {"username": "Panchito"})
        response = self.client.post(f"{USERS_ENDPOINT}login/", {"username": "Panchito"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Welcome Panchito"})
        self.assertEqual(response.cookies["sessionid"].value, "Panchito")
