import datetime

runtime = datetime.datetime.now().date()


def test_bills():
    bills = open('billshist.txt', 'r')
    for line in format_bills(bills.readlines()):
        print(line)
    print('\n')
    reads = open('readshist.txt', 'r')
    for line in format_reads(reads.readlines()):
        print(line)


# returns one string containing newline-delimted lines.
def format_bills(bills):
    result = []
    result.append('{0:<12} {1:>8} {2:>10}'.format('run date', 'bill date', 'amount '))
    for bill in bills[2:]:
        line = bill.split(' ')
        if len(line) > 3:
            result.append('{0:<12} {1:>8} {2:>10}'.format(str(runtime), line[1], line[2]))
    return '\n'.join(result)


# returns one string containing newline-delimted lines.
def format_reads(reads):
    result = []
    result.append('{0:<12} {1:>8} {2:>10} {3:>10}'.format('run date', 'month', 'month', 'usage'))
    for read in reads[4:]:
        line = read.strip().split(' ')
        if len(line) > 4:
            result.append('{0:<12} {1:>8} {2:>10} {3:>10}'.format(str(runtime), line[0], line[1], line[2]))
    return '\n'.join(result)


