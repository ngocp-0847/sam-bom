import json
import uuid
import boto3
import requests
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
import os

def lambda_handler(event, context):
    """Sample pure Lambda function
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('questions')
    
    if event['httpMethod'] == 'GET':
        if event['path'] == '/item':
            resp = table.scan()
            body = json.dumps({
                "message": "hello world bombay",
                "data": resp['Items']
            })
        elif event['path'] == '/item/search':

            endpoint = os.getenv('ES_ENDPOINT')
            region = os.getenv('ES_REGION')
            # Below code will be used while sending a request  
            headers = {"Content-Type": "application/json"}
            creds = boto3.Session().get_credentials()
            awsauth = AWS4Auth(creds.access_key, creds.secret_key, region, 'es', session_token=creds.token)
            index = 'item'
            search = event['queryStringParameters']['text']
            print('params search', event['queryStringParameters'])
            query = {
                    "query":{
                        "multi_match" : {
                            "query":  search, 
                            "fields": [ "Question", "Answer" ] 
                        }
                    },
                    "size": 10000    
                }
            url = endpoint + '/' + index + '/_search'
            response = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
            print('response', response.text)
            
            responseObj = json.loads(response.text)
            responseData = responseObj['hits']['hits']
            body = json.dumps({
                "message": "search OK",
                "data": responseData
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
