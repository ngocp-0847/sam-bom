import json
import uuid
import boto3
import requests
import os

s3 = boto3.client('s3')

apiEndpoint = 'https://tt66tt'
s3bucket = 'bomt3r-website-bucket'
objectOriginal = s3.get_object(Bucket=s3bucket, Key='index.html')
content = objectOriginal['Body'].read().decode("utf-8")
content = content.replace("${API_ENDPOINT}", apiEndpoint)

objectIndexFile = s3.put_object(Bucket=s3bucket, Key='index.html', Body=content,
    ACL='public-read', ContentType='text/html')
print(objectIndexFile)


