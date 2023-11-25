from rest_framework.test import APITestCase
from users.models import User
from links.models import Link
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class TestLinks(APITestCase):
    COMMON_USERNAME = "test"
    COMMON_PASSWORD = "test1234"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin1234"

    SIGNUP_URL = "http://127.0.0.1:8000/api/v1/users/"
    SIGNIN_URL = "http://127.0.0.1:8000/api/v1/users/signin"

    ALL_LINKS_URL = "http://127.0.0.1:8000/api/v1/links/all"
    ADD_LINK_URL = "http://127.0.0.1:8000/api/v1/links/addlink"

    def setUp(self):
        common_user = User.objects.create(username=self.COMMON_USERNAME)
        common_user.set_password(self.COMMON_PASSWORD)
        common_user.save()

        admin_user = User.objects.create(username=self.ADMIN_USERNAME)
        admin_user.set_password(self.ADMIN_PASSWORD)
        admin_user.is_staff = True
        admin_user.save()

        Link.objects.create(
            link=env("MY_WEB_HOOK_LINK"),
            owner=common_user,
        )

    def test_add_link_without_authentication(self):
        response = self.client.post(
            self.ADD_LINK_URL,
            data={
                "link": env("MY_WEB_HOOK_LINK"),
            },
        )

        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 403.",
        )

    def test_add_link_with_authentication(self):
        user = User.objects.get(username=self.ADMIN_USERNAME)
        self.client.force_login(user)

        response = self.client.post(
            self.ADD_LINK_URL,
            data={
                "link": env("MY_WEB_HOOK_LINK"),
            },
        )

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

    def test_all_links_with_common_user(self):
        user = User.objects.get(username=self.COMMON_USERNAME)
        self.client.force_login(user)

        response = self.client.get(self.ALL_LINKS_URL)
        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 403.",
        )

    def test_all_links_with_admin_user(self):
        user = User.objects.get(username=self.ADMIN_USERNAME)
        self.client.force_login(user)

        response = self.client.get(self.ALL_LINKS_URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertEqual(
            len(data),
            1,
        )

    def test_one_link(self):
        pass
