import datetime

runtime = datetime.datetime.now().date()


# rows: dicts from the Billing export (Start date, End date, Billed amount, HCF).
# returns one string containing newline-delimted lines.
def format_bills(rows):
    result = ['{0:<12} {1:<24} {2:>10}'.format('run date', 'bill period', 'amount')]
    for r in rows:
        period = '{0} - {1}'.format(r['Start date'].strip(), r['End date'].strip())
        result.append('{0:<12} {1:<24} {2:>10}'.format(str(runtime), period, r['Billed amount'].strip()))
    return '\n'.join(result)


# returns one string containing newline-delimted lines.
def format_reads(rows):
    result = ['{0:<12} {1:<24} {2:>10}'.format('run date', 'bill period', 'usage (HCF)')]
    for r in rows:
        period = '{0} - {1}'.format(r['Start date'].strip(), r['End date'].strip())
        result.append('{0:<12} {1:<24} {2:>10}'.format(str(runtime), period, r['HCF'].strip()))
    return '\n'.join(result)
