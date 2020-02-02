from flask import Flask
from flask import request
from flask import jsonify
import os
import json
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello, World! This is a Scale demo by Josie Barth.'

@app.route('/scale/callback', methods=['POST']) 
def writeScaleTaskToS3():

    print("In /scale/callback")

    ## Initialize S3 client
    s3_client = boto3.client('s3',
        aws_access_key_id=os.environ['S3_ACCESS_KEY'], 
        aws_secret_access_key=os.environ['S3_SECRET_KEY'], 
        region_name=os.environ['S3_REGION']
    )

    print("Init S3")

    print(request)
    
    ## Grab the callback JSON task sent from Scale
    task_json = request.get_json()
    print(task_json)

    task_id = task_json.get('task_id')
    print(task_id)

    task_json_serialized = json.dumps(task_json)
    print(task_json_serialized)

    try:

        print("Write to S3")

        ## Write the task to S3
        response = s3_client.put_object(
            Bucket=os.environ['S3_BUCKET_NAME'],
            Key=task_id,
            Body=task_json_serialized
        );
        return jsonify([{'status':200, 'message':'Scale task written to S3'}])
    except ClientError as e: 
        print("Fail write to S3")

        ## Log in case of error
        print(e)
        return jsonify([{'status':400, 'error':'Something went wrong writing scale task to S3'}])
