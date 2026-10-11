import os

# set LOCAL=1 (e.g. in .env) to skip AWS: files are written to ./data and notifications are printed.
LOCAL = os.environ.get('LOCAL', '').lower() in ('1', 'true', 'yes')

# initialize aws connection.
# credentials are loaded from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
print('aws dal starting... (local mode)' if LOCAL else 'aws dal starting...')
if not LOCAL:
    import boto3
    s3 = boto3.resource('s3')
    sns = boto3.client('sns')


# write text data to the S3 bucket. this function handles conversion to binary.
# input is the key one line containing a newline-delimited data set.
# use the S3 versioning if history should be kept - this function will write with the same key on each run.
def put_list(key, data):
    put_text(key, '\n'.join(data))


def put_text(key, data):
    if LOCAL:
        os.makedirs('data', exist_ok=True)
        with open(os.path.join('data', key), 'w') as f:
            f.write(data)
        print('written locally: data/' + key)
        return
    bdata = bytes(data, 'utf-8')
    s3.Bucket('dep-history').put_object(Key=key, Body=bdata)
    print('written to s3: ' + key)


# get config data from s3
def get_config():
    # s3.Bucket('dep-config').download_file('aws.config', '')
    object = s3.Object('dep-config', 'aws.config').get()
    body_data = object['Body'].read().decode('utf-8')
    return body_data


# addresses is a list of email addresses.
# items should be a list - first item is the meter read history and 2nd is the bill history.
# each item is a newline-delimited text field.
def send(items):
    data = '\n'.join(['Meter Reads', items[0], '', '', 'Bill History', items[1]])
    if LOCAL:
        print('--- email (not sent) ---\n' + data)
        return
    resp = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:397678393215:dep-notifications',
        Subject='DEP Bill Extract',
        Message=data
    )
    print('email sent', resp)


def send_daily(msg):
    print('sending daily:' + ' '.join(msg))
    if LOCAL:
        print('--- email (not sent) ---\n' + '\n'.join(msg))
        return
    resp = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:397678393215:dep-notifications',
        Subject='DEP Bill Extract',
        Message='\n'.join(msg)
    )
    print('email sent', resp)


