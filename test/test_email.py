import unittest
import aws
import scrape


class TestEmail(unittest.TestCase):

    def test_mnthly_email(self):
        params = []
        ml = open('../data/reads-fmt.txt', 'r').readlines()
        reads = ''.join(ml)
        params.append(reads)
        bl = open('../data/bills-fmt.txt', 'r').readlines()
        bills = ''.join(bl)
        ml.close()
        bl.close()
        params.append(bills)
        aws.send(reads, bills)

    def test_daily_email(self):
        f = open('daily_reads_element.txt')
        reads = f.readlines()
        f.close()
        msg = scrape.format_daily_usage(reads)
        aws.send_daily(msg)


if __name__ == '__main__':
    unittest.main()