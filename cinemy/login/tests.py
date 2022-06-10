from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthenticationTest(TestCase):
    def test_login(self):
        User = get_user_model()
        User.objects.create_user("temporary", "temporary@gmail.com", "temporary")
        self.client.login(username="temporary", password="temporary")
        response = self.client.get("/", follow=True)
        self.assertEqual(
            response.context["user"].username, "temporary", "Login has failed"
        )

    def test_logout(self):
        User = get_user_model()
        User.objects.create_user("temporary", "temporary@gmail.com", "temporary")
        self.client.login(username="temporary", password="temporary")
        self.client.logout()
        response = self.client.get("")
        self.assertTrue("Login" in str(response.content), "Logout has failed")
