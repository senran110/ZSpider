import unittest


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


person = {'name': 'Nike'}
numbers = [1, 3, 4, 88]
s = "codelife"


class MyTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(8, add(5, 3))

    def test_subtract(self):
        self.assertEqual(2, subtract(5, 3))

    def test_assert_method(self):
        self.assertIn("code", s)
        self.assertIsNone(person.get('Name', None))
        self.assertIsInstance(numbers[0], str)


class Calculator(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y

    def subtract(self):
        return self.x - self.y


class CalculatorTest(unittest.TestCase):
    def setUp(self):
        self.c = Calculator(5, 3)

    def test_add(self):
        self.assertEqual(8, self.c.add())

    def tearDown(self):
        del self.c


if __name__ == '__main__':
    unittest.main()
