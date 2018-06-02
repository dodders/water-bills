# water-bills

scrape DEP website for water bill info; store in S3 buckets and email via SNS.

dependencies:
* pipenv
* python 3.6
* selenium 
* headless chrome
* boto3 (python aws libraries)
* docker

### processing

the python script uses selenium + headless chrome to login to the DEP website and collect 1) meter reading history (water usage) and 2) quarterly billing amounts.

it stores the parsed data in two files (one for bills, one for history) in an s3 bucket. it replaces the files on each run, using the S3 bucket history to maintain history. the bucket is not public.

it formats the bills and usage into a readable format and uses AWS SNS to send the data to a notification ARN - this is set up with email subscriptions for distribution.

### environments
#### local
all sensitive data is stored locally in a .env file that is not checked into github. the code should run using

```bash
pipenv run python3 main.sh
```
the build-docker.sh script will build a docker container that can also be run locally.
 
#### aws
in aws the secrets are specified as environment variables in the job definition.
aws batch is used to run the container with logs written to cloudwatch.

### todo
* schedule to run each month using cloudwatch events.
* implement retry handling and alerting for failures. 
