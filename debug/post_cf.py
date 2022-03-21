import urllib3
import json

SUCCESS = "SUCCESS"
FAILED = "FAILED"

http = urllib3.PoolManager()


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {
        'Status' : responseStatus,
        'Reason' : event['Reason'],
        'PhysicalResourceId' : physicalResourceId,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)


    except Exception as e:

        print("send(..) failed executing http.request(..):", e)


event = {
    'ResponseURL': 'https://cloudformation-custom-resource-response-useast2.s3.us-east-2.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-2%3A360631776925%3Astack/check-custom/e8512830-a822-11ec-b736-06c484fea778%7CS3ChangeUrlResource%7C7b2a5e9d-5823-4cd8-9309-e31b384418f6?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220320T080618Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=AKIAVRFIPK6PGS2LKJGU%2F20220320%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=40db31c742627f917bffb22e0e1258448a9114b86c4d56018d4b0a4677f16f74',
    'StackId': 'arn:aws:cloudformation:us-east-2:360631776925:stack/check-custom/e8512830-a822-11ec-b736-06c484fea778',
    'RequestId': '7b2a5e9d-5823-4cd8-9309-e31b384418f6',
    'LogicalResourceId': 'S3ChangeUrlResource',
    'PhysicalResourceId' : 'check-custom-S3ChangeUrlResource-30RX5BC3OI7D',
    'Reason' : 'nothing',
}

send(event, '', 'SUCCESS', {}, event['PhysicalResourceId'])