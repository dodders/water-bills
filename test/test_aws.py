import unittest
import aws


class TestAws(unittest.TestCase):

    def test_s3get(self):
        ret = aws.get_config();
        print('ret is: ', ret)


if __name__ == '__main__':
    unittest.main()