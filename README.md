# Mục đích
- Để test SAM application serverless, cloudformation. Phục vụ mục đích học tập

**Các mục kiến thức cần lưu ý**
- Cloud formation + SAM deploy and package serverless
- Dùng AWS::CloudFormation::CustomResource để khi deploy sẽ change base url (của API Gateway) vào trong file **index.html** của s3 bucket

# QAnswer-app

![](doc/aws-describe.png?raw=true)

# Check stack elasticsearch, check data
- check exist index
curl  ES_DOMAIN/_aliases
curl ES_DOMAIN/_cat/indices?v

- check mapping
curl  ES_DOMAIN/item

- check item 
curl  ES_DOMAIN/item/_search

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
sam-bom1$ sam build --use-container
```

## Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
sam local start-api
http://localhost:3000/
```
## Fetch, tail, and filter Lambda function logs


```bash
sam logs -n HelloWorldFunction --stack-name sam-bom1 --tail
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name sam-bom1
```
