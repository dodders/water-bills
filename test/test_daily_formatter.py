import unittest
import scrape

DAILY_CSV = '''﻿Service,Time period,Consumption,Consumption unit,Approximate charge,Meter serial number,Register serial number,Counter time frame,Index,Index unit
S1, Oct 1 2026,2,100 CF,22.28,M1,,SINGLE REG,2853,100 CF
S1, Oct 2 2026,0,100 CF,0,M1,,SINGLE REG,2853,100 CF
S1, Oct 3 2026,0,100 CF,0,M1,,SINGLE REG,0,
'''


class TestFormatter(unittest.TestCase):

    def test_daily_skips_future_days(self):
        lines = scrape.format_daily_usage(scrape.parse_csv(DAILY_CSV))
        self.assertEqual(lines[0], 'daily meter readings!')
        self.assertEqual(len(lines), 3)
        self.assertIn('Oct 1 2026', lines[1])
        self.assertIn('22.28', lines[1])


if __name__ == '__main__':
    unittest.main()
