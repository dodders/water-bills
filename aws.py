import os
import smtplib
from email.message import EmailMessage

# set LOCAL=1 (e.g. in .env) to skip AWS: files are written to ./data and notifications are printed,
# or emailed over SMTP if SMTP_HOST is set (also needs SMTP_USER, SMTP_PASSWORD, MAIL_FROM, MAIL_TO;
# SMTP_PORT defaults to 587/STARTTLS; MAIL_TO may be comma-separated).
LOCAL = os.environ.get('LOCAL', '').lower() in ('1', 'true', 'yes')

# initialize aws connection.
# credentials are loaded from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
print('aws dal starting... (local mode)' if LOCAL else 'aws dal starting...')
if not LOCAL:
    import boto3
    s3 = boto3.resource('s3')
    sns = boto3.client('sns')


def local_notify(subject, body):
    host = os.environ.get('SMTP_HOST')
    if not host:
        print('--- email (not sent) ---\n' + body)
        return
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ['MAIL_FROM']
    msg['To'] = os.environ['MAIL_TO']
    msg.set_content(body)
    with smtplib.SMTP(host, int(os.environ.get('SMTP_PORT', '587'))) as smtp:
        smtp.starttls()
        smtp.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
        smtp.send_message(msg)
    print('email sent via smtp to', msg['To'])


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
        local_notify('DEP Bill Extract', data)
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
        local_notify('DEP Bill Extract', '\n'.join(msg))
        return
    resp = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:397678393215:dep-notifications',
        Subject='DEP Bill Extract',
        Message='\n'.join(msg)
    )
    print('email sent', resp)


