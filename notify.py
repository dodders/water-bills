import os
import smtplib
from email.message import EmailMessage


# write text data to ./data/<key>. the nightly workflow uploads these files as an artifact.
# put_list takes a list of lines.
def put_list(key, data):
    put_text(key, '\n'.join(data))


def put_text(key, data):
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', key), 'w') as f:
        f.write(data)
    print('written locally: data/' + key)


# items should be a list - first item is the meter read history and 2nd is the bill history.
# each item is a newline-delimited text field.
def send(items):
    deliver('DEP Bill Extract', '\n'.join(['Meter Reads', items[0], '', '', 'Bill History', items[1]]))


def send_daily(msg):
    deliver('DEP Bill Extract', '\n'.join(msg))


# emails the body over SMTP if SMTP_HOST is set (also needs SMTP_USER, SMTP_PASSWORD, MAIL_FROM, MAIL_TO;
# SMTP_PORT defaults to 587/STARTTLS; MAIL_TO may be comma-separated). otherwise prints it.
def deliver(subject, body):
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
