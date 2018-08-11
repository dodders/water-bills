import unittest
import scrape
from dotenv import load_dotenv


class TestScrape(unittest.TestCase):

    @unittest.skip('not needed for now.')
    def test_monthly(self):
        print('testing monthly...')
        load_dotenv()
        # ret = scrape_daily_usage()
        ret = scrape.scrape_monthly()
        print(ret)
        print('done.')

    def test_daily(self):
        print('testing daily...')
        load_dotenv()
        ret = scrape.scrape_daily_usage()
        print(ret)
        print('done.')


if __name__ == '__main__':
    unittest.main()
