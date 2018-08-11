import scrape
import unittest


class TestFormatter(unittest.TestCase):

    def test_fmt(self):
        f = open('daily_reads_element.txt')
        reads = f.readlines()
        f.close()
        ret = scrape.format_daily_usage(reads)
        print(ret)


if __name__ == '__main__':
    unittest.main()
