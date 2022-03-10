import json
import uuid
import boto3
# import requests
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('questions')
    
    if event['httpMethod'] == 'GET':
        resp = table.scan()
        body = json.dumps({
            "message": "hello world bombay",
            "data": resp['Items']
        })
    elif event['httpMethod'] == 'POST':
        dataInput = json.loads(event['body']);
        resp = table.put_item(
            Item={
                'Id': str(uuid.uuid4()),
                'Question': dataInput['question'],
                'Answer': dataInput['answer'],
            }
        )
        body = json.dumps({
            "message": "hello world bombay",
            "data": resp
        })

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": body,
    }
