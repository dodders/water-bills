import boto3

# initialize aws connection.
# credentials are loaded from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
print('aws dal starting...')
s3 = boto3.resource('s3')
sns = boto3.client('sns')


# write text data to the S3 bucket. this function handles conversion to binary.
# input is the key one line containing a newline-delimited data set.
# use the S3 versioning if history should be kept - this function will write with the same key on each run.
def put_text(key, data):
    bdata = bytes(data, 'utf-8')
    s3.Bucket('dep-history').put_object(Key=key, Body=bdata)


# addresses is a list of email addresses.
# items should be a list - first item is the meter read history and 2nd is the bill history.
# each item is a newline-delimited text field.
def send(items):
    data = '\n'.join(['Meter Reads', items[0], '', '', 'Bill History', items[1]])
    resp = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:397678393215:dep-notifications',
        Subject='DEP Bill Extract',
        Message=data
    )
    print('email sent', resp)


def test_email():
    params=[]
    ml = open('reads-fmt.txt', 'r').readlines()
    reads = ''.join(ml)
    params.append(reads)
    bl = open('bills-fmt.txt', 'r').readlines()
    bills = ''.join(bl)
    params.append(bills)

    email_results(params)


