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

    ## Initialize S3 client
    s3_client = boto3.client('s3',
        aws_access_key_id=os.environ['S3_ACCESS_KEY'], 
        aws_secret_access_key=os.environ['S3_SECRET_KEY'], 
        region_name=os.environ['S3_REGION']
    )
    
    ## Grab the callback JSON task sent from Scale
    task_json = request.get_json()
    task_id = task_json.get('task_id')
    task_json_serialized = json.dumps(task_json)

    try:
        ## Write the task to S3
        response = s3_client.put_object(
            Bucket=os.environ['S3_BUCKET_NAME'],
            Key=task_id,
            Body=task_json_serialized
        );
        return jsonify([{'status':200, 'message':'Scale task written to S3'}])
    except ClientError as e: 
        ## Log in case of error
        print(e)
        return jsonify([{'status':400, 'error':'Something went wrong writing scale task to S3'}])
