import scrape
import aws
import format

# returns a list of 2 results - consumption and bills (in that order)
print('scraping...')
data = scrape.scrape_monthly()

print('formatting reads...')
reads = format.format_reads(data[0])
print('writing reads...')
aws.put_text('reads.txt', reads)

print('formatting bills...')
bills = format.format_bills(data[1])
print('writing bills...')
aws.put_text('bills.txt', bills)

params = [reads, bills]
aws.send(params)

print('done.')
