from unittest import TestCase
from unittest.mock import MagicMock, Mock

import ornitho
from ornitho import (
    APIException,
    APIRequester,
    AuthenticationException,
    GatewayTimeoutException,
)


class TestAPIRequester(TestCase):
    def setUp(self):
        self.requester = APIRequester()

    def test_enter(self):
        requester = self.requester.__enter__()
        self.assertEqual(requester, self.requester)

    def test_exit(self):
        self.requester.close = Mock()
        self.requester.__exit__()
        self.requester.close.assert_called()

    def test_close(self):
        self.requester.session = Mock()
        self.requester.close()
        self.requester.session.close.assert_called()

    def test_request(self):
        # Case 1: no data key
        self.requester.request_raw = MagicMock(
            return_value=[[{"id": "1"}, {"id": "2"}], None]
        )
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [{"id": "1"}, {"id": "2"}])
        self.assertEqual(pk, None)

        # Case 2: data is list
        self.requester.request_raw = MagicMock(
            return_value=[{"data": [{"id": "1"}, {"id": "2"}]}, None]
        )
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [{"id": "1"}, {"id": "2"}])
        self.assertEqual(pk, None)

        # Case 3: data is dict
        self.requester.request_raw = MagicMock(
            return_value=[
                {"data": {"sightings": [], "forms": [{"sightings": [{"id": "1"}]}]}},
                "pagination_key",
            ]
        )
        response, pk = self.requester.request(method="post", url="test")
        self.assertEqual(response, [{"id": "1"}])
        self.assertEqual(pk, "pagination_key")

        # Case 4: request all
        self.requester.request_raw = MagicMock(
            side_effect=[
                [{"data": [{"id": "1"}]}, "pagination_key"],
                [{"data": []}, "pagination_key"],
            ]
        )
        response, pk = self.requester.request(
            method="get", url="test", pagination_key="pagination_key", request_all=True
        )
        self.assertEqual(response, [{"id": "1"}])
        self.assertEqual(pk, "pagination_key")

    def test_handle_error_response(self):
        self.assertRaises(
            AuthenticationException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=401)
            ),
        )
        self.assertRaises(
            GatewayTimeoutException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=504)
            ),
        )
        self.assertRaises(
            APIException,
            lambda: self.requester.handle_error_response(response=Mock(status_code=0)),
        )

    def test_request_headers(self):
        headers = self.requester.request_headers()
        self.assertEqual(
            headers, {"User-Agent": f"API Python Client/{ornitho.__version__}"}
        )

    def test_request_raw(self):

        # Case 1: GET Method
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={"pagination_key": "new_key"},
                content=b'{"data": [{"id": "1"}]}',
            )
        )
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": "param"},
            body={"test": "filter"},
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")

        # Case 2: Other Method
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200, headers={}, content=b'{"data": [{"id": "1"}]}'
            )
        )
        response, pk = self.requester.request_raw(
            method="post", url="test", pagination_key="key", body={"test": "filter"}
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, None)

        # Case 3: Error
        self.requester.session.request = MagicMock(return_value=Mock(status_code=401))
        self.assertRaises(
            Exception, lambda: self.requester.request_raw(method="post", url="test")
        )
