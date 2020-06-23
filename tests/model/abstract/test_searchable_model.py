from unittest import TestCase, mock

import ornitho
from ornitho.model.abstract.searchable_model import SearchableModel

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestSearchableModel(TestCase):
    class MyModel(SearchableModel):

        ENDPOINT = "my_model"

        @classmethod
        def create_from_ornitho_json(cls, data):
            identifier: int = int(data["id"])
            obj = cls(identifier)
            obj._raw_data = data
            return obj

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return [[{"id": "1"}, {"id": "2"}], "paginationKey"]

    @mock.patch.object(ornitho.api_requester.APIRequester, "request", fake_request)
    def test_search(self):
        models, pk = self.MyModel.search()
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].id_, 1)
        self.assertEqual(models[1].id_, 2)
        self.assertEqual(pk, "paginationKey")

    @mock.patch.object(ornitho.api_requester.APIRequester, "request", fake_request)
    def test_search_all(self):
        models = self.MyModel.search_all()
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0].id_, 1)
        self.assertEqual(models[1].id_, 2)
