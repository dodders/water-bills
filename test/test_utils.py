import utils
import unittest


class TestUtils(unittest.TestCase):

    def test_decode(self):
        data = "KEY=VALUE\nKEY2=VALUE2\nusr=dodders"
        print(data)


if __name__ == '__main__':
    unittest.main()

