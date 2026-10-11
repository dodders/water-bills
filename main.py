from dotenv import load_dotenv
load_dotenv()

import scrape
import notify
import format


def monthly():
    # returns a list of 2 results - consumption and bills (in that order)
    print('scraping...')
    data = scrape.scrape_monthly()

    print('formatting reads...')
    reads = format.format_reads(data[0])
    print('writing reads...')
    notify.put_text('reads.txt', reads)

    print('formatting bills...')
    bills = format.format_bills(data[1])
    print('writing bills...')
    notify.put_text('bills.txt', bills)

    params = [reads, bills]
    notify.send(params)

    print('monthly done.')


def daily():
    print('scraping daily...')
    reads = scrape.scrape_daily_usage()
    print('writing reads...')
    notify.put_list('daily_reads.txt', reads)
    print('emailing...')
    notify.send_daily(reads)
    print('daily done.')


if __name__ == '__main__':
    daily()
