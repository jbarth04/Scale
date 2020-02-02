from flask import Flask
from flask import request
from flask import jsonify
import os
import json
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

## Index page, nothing fancy here
@app.route('/')
def helloWorld():
    return 'Hello, World! This is a Scale demo by Josie Barth.'

## POST endpoint for Scale callback
## Input: JSON body of task from Scale
## Returns: 200 if task was written to S3,
##          400 if bad request,
##          500 if an error writing to S3
@app.route('/scale/callback', methods=['POST']) 
def writeScaleTaskToS3():

    ## Grab the JSON task sent from Scale
    task_json = request.get_json(force=True)
    task_id = task_json.get('task_id')
    task_json_serialized = json.dumps(task_json)

    ## Initialize S3 client
    s3_client = getS3Client()

    try:
        ## Write the task to S3
        response = s3_client.put_object(
            Bucket=os.environ['S3_BUCKET_NAME'],
            Key=task_id,
            Body=task_json_serialized
        );
        return jsonify([{'status':200, 'message':'Scale task written to S3'}]) 
    except ClientError as e: 
        ## Log error
        print(e)
        return jsonify([{'status':500, 'error':'Something went wrong writing scale task to S3'}])

## GET endpoint fetch Scale task that been written to S3
## Input: Scale task_id
## Returns: 200 and task if found,
##          404 if task not found,
##          500 if error reading from S3
@app.route('/scale/task/<task_id>', methods=['GET'])
def getScaleTaskFromS3(task_id):

    if isEmpty(task_id):
        return jsonify([{'status':400, 'error':'task_id cannot be empty or blank'}])

    ## Initialize S3 client
    s3_client = getS3Client()

    try:
        ## Get task from S3
        response = s3_client.get_object(
            Bucket=os.environ['S3_BUCKET_NAME'],
            Key=task_id
        );

        task_json = response['Body'].read().decode('utf-8') 
        return jsonify([{'status':200, 'message':'Scale task found in S3', 'task':task_json}])
    except ClientError as e: 
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            return jsonify([{'status':404, 'error': 'task_id {} not found'.format(task_id)}])

        ## Log non-NoSuchKey error
        print(e)
        return jsonify([{'status':500, 'error':'Something went wrong reading scale task from S3'}])

## Returns initialized S3 client
## Set following variables in your env to run locally (with values filled in)
##  export S3_ACCESS_KEY="your_s3_access_key"
##  export S3_ACCESS_KEY="your_s3_secret_key"
##  export S3_ACCESS_KEY="your_s3_region"
def getS3Client():
    return boto3.client('s3',
        aws_access_key_id=os.environ['S3_ACCESS_KEY'],
        aws_secret_access_key=os.environ['S3_SECRET_KEY'],
        region_name=os.environ['S3_REGION']
    )

## Borrowed from https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
def isEmpty(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
