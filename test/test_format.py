import unittest
import format
import scrape

BILLS_CSV = '''﻿Start date,End date,Billed amount,HCF
 Sep 2 2025, Sep 30 2025,196.19,15
 Jul 1 2026, Aug 31 2026,498.83,36'''


class TestFormat(unittest.TestCase):

    def setUp(self):
        self.rows = scrape.parse_csv(BILLS_CSV)

    def test_bills(self):
        lines = format.format_bills(self.rows).split('\n')
        self.assertEqual(len(lines), 3)
        self.assertIn('Sep 2 2025 - Sep 30 2025', lines[1])
        self.assertTrue(lines[2].endswith('498.83'))

    def test_reads(self):
        lines = format.format_reads(self.rows).split('\n')
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[1].endswith('15'))


if __name__ == '__main__':
    unittest.main()
