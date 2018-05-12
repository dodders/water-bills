import psycopg2
import datetime

conn = psycopg2.connect("dbname=depdb user=george")
cur = conn.cursor()
runtime = datetime.datetime.now()

bf = open('billshist.txt')
rf = open('readshist.txt')

bills = bf.readlines()
reads = rf.readlines()


for bill in bills[2:]:
    line = bill.split(' ')
    if len(line) > 3:
        cur.execute('insert into bill_history (inserted, bill_date, amount) values(%s, %s, %s)',
                    (runtime, line[1], line[2]))
        conn.commit()

for read in reads[4:]:
    line = read.strip().split(' ')
    if len(line) > 4:
        cur.execute('insert into readings (inserted, month, reading, consumption) values(%s, %s, %s, %s)',
                    (runtime, line[0], line[2], line[5]))
        conn.commit()

cur.close()
conn.close()
