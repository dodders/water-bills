import boto3

# initialize aws connection.
# credentials are loaded from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
print('aws dal starting...')
s3 = boto3.resource('s3')


# write text data to the S3 bucket. this function handles conversion to binary.
def put_text(key, text):
    btext = bytes(text, 'utf-8')
    s3.Bucket('dep-history').put_object(Key=key, Body=btext)



