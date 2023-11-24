from rest_framework.test import APITestCase
from .models import Info
import environ
import datetime as dt

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


def returnToday():
    d = dt.datetime.now()
    return f"{d.year}-{d.month}-{d.day}"


class TestInfos(APITestCase):
    TYPE = "general"
    TITLE = "info test"
    HREF = "info href"
    DATE = returnToday()
    EXPIRED_DATE = "2023-01-01"

    GET_SECRET = env("GET_SECRET_KEY")
    POST_SECRET = env("POST_SECRET_KEY")

    URL = "http://127.0.0.1:8000/api/v1/infos/all/"

    def setUp(self):
        Info.objects.create(
            info_type=self.TYPE,
            title=self.TITLE,
            href=self.HREF,
            date=self.DATE,
        )

    def test_all_infos(self):
        response = self.client.get(self.URL + self.GET_SECRET)
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

    def test_with_fake_get_secret(self):
        response = self.client.get(self.URL + "fake_secret")

        self.assertEqual(
            response.status_code,
            400,
            "Status code isn't 400.",
        )

    def test_create_info(self):
        new_info_type = "general"
        new_title = "New title"
        new_href = "New href"
        new_date = returnToday()

        response = self.client.post(
            self.URL + self.POST_SECRET,
            data={
                "info_type": new_info_type,
                "title": new_title,
                "href": new_href,
                "date": new_date,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertEqual(
            data["info_type"],
            new_info_type,
        )
        self.assertEqual(
            data["title"],
            new_title,
        )
        self.assertEqual(
            data["href"],
            new_href,
        )
        self.assertEqual(
            data["date"],
            new_date,
        )

    def test_clean_expired_infos(self):
        response = self.client.get(self.URL + self.GET_SECRET)
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

        Info.objects.create(
            info_type=self.TYPE,
            title=self.TITLE,
            href=self.HREF,
            date=self.EXPIRED_DATE,
        )

        response = self.client.get(self.URL + self.GET_SECRET)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertEqual(
            len(data),
            2,
        )

        new_info_type = "general"
        new_title = "New title"
        new_href = "New href"
        new_date = returnToday()

        self.client.post(
            self.URL + self.POST_SECRET,
            data={
                "info_type": new_info_type,
                "title": new_title,
                "href": new_href,
                "date": new_date,
            },
        )

        response = self.client.get(self.URL + self.GET_SECRET)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertEqual(
            len(data),
            2,
        )

    def test_with_fake_post_secret(self):
        response = self.client.post(
            self.URL + "fake_secret",
            data={
                "info_type": self.TYPE,
                "title": self.TITLE,
                "href": self.HREF,
                "date": self.DATE,
            },
        )

        self.assertEqual(
            response.status_code,
            400,
            "Status code isn't 400.",
        )
