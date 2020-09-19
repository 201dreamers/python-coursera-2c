import unittest


def factorize(x: int):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        subtests_data = ('string', 1.5)
        for x in subtests_data:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        subtests_data = (-1, -10, -100)
        for x in subtests_data:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        with self.subTest(x=0):
            self.assertCountEqual(factorize(0), (0,))

        with self.subTest(x=1):
            self.assertCountEqual(factorize(1), (1,))

    def test_simple_numbers(self):
        subtests_data = {
            3: (3,),
            13: (13,),
            29: (29,)
        }
        for x, out_data in subtests_data.items():
            with self.subTest(x=x):
                self.assertCountEqual(factorize(x), out_data)

    def test_two_simple_multipliers(self):
        subtests_data = {
            6: (2, 3),
            26: (2, 13),
            121: (11, 11)
        }
        for x, out_data in subtests_data.items():
            with self.subTest(x=x):
                self.assertCountEqual(factorize(x), out_data)

    def test_many_multipliers(self):
        subtests_data = {
            1001: (7, 11, 13),
            9699690: (2, 3, 5, 7, 11, 13, 17, 19)
        }
        for x, out_data in subtests_data.items():
            with self.subTest(x=x):
                self.assertCountEqual(factorize(x), out_data)

