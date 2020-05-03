import unittest

from util.redis_client import RedisClient


class RedisOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self.op = RedisClient()

    def test_count(self):
        self.assertIsInstance(self.op.count(), int)


if __name__ == '__main__':
    unittest.main()
