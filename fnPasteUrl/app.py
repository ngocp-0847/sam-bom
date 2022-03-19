import json
import uuid
import boto3
import requests
import os

def getResponse(event, context, responseStatus):
    responseBody = {'Status': responseStatus,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    }
    responseBody = json.dumps(responseBody)
    print('RESPONSE BODY:', responseBody)
    return responseBody

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    try:
        if event['RequestType'] == 'Delete':
            print('Deleted!')
            req = requests.put(event['ResponseURL'], data=getResponse(event, context, 'SUCCESS'))
            return
        apiEndpoint = event['ResourceProperties']['API_ENDPOINT']
        s3bucket = event['ResourceProperties']['S3_BUCKET']
        objectOriginal = s3.get_object(Bucket=s3bucket, Key='index.html')
        content = objectOriginal['Body'].read().decode("utf-8")
        content = content.replace("${API_ENDPOINT}", apiEndpoint)
        print('New content', content)
        objectIndexFile = s3.put_object(Bucket=s3bucket, Key='index.html', Body=content,
            ACL='public-read', ContentType='text/html')
        print(objectIndexFile)

        responseData = {}
        responseData['Data'] = objectIndexFile
        req = requests.put(event['ResponseURL'], data=getResponse(event, context, 'SUCCESS'))
        print(req)

    except Exception as err:
        print('error:', err)
        req = requests.put(event['ResponseURL'], data=getResponse(event, context, 'FAILED'))
        print(req)
