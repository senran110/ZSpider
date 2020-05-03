import unittest

from web_api.api import app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self._app = app.test_client()

    def test_get(self):
        r = self._app.get('/random')
        assert ':' in str(r.data)


if __name__ == '__main__':
    unittest.main()
