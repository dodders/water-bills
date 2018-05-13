import scrape
import aws
import format


# returns a list of 2 results - consumption and bills (in that order)
data = scrape.scrape_data()

cons = format.format_reads(data[0])
for line in cons:
    print(line)

bills = format.format_bills(data[1])
for line in bills:
    print(line)