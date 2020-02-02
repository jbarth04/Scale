# ScaleAPI Demo

## Preface
In browsing the Scale API docs, I noticed that the python sample callback server implementation is still in the works (as of Feb 2nd, 2020), https://scale.com/docs?python#callbacks.  I decided it would be a fun exercise to set up an example callback server with a `POST` endpoint that consumes the result of a Scale task and writes it to Amazon S3, and a `GET` endpoint to read those tasks and verify it works.

## A simple python callback server for Scale API tasks

This demo project includes the server code [scale.py](https://github.com/jbarth04/Scale/blob/master/scale.py) that is running live on Heroku at https://scale-demo.herokuapp.com/.  You hit the callback server and verify it works by following these steps:

1. Take a sample request from Scale API docs https://scale.com/docs?python#introduction and set the callback to `https://scale-demo.herokuapp.com/scale/callback`.  Examples below: 

    - Clone this repo, set `export SCALE_API_KEY="your_scale_api_key"` in your local env, and run the python script [ScalePolygonAnnotation.py](https://github.com/jbarth04/Scale/blob/master/ScalePolygonAnnotation.py) (`$ python3 ScalePolygonAnnotation.py`).  You'll get a response in the format `{'task_id': '123456789'}`.  Copy the `task_id` value.
    
    - Run this cURL command and copy the returned `task_id` value.
    ```
      curl "https://api.scale.com/v1/task/polygonannotation" \
      -u "YOUR_SCALE_API_KEY:" \
      -d callback_url="https://scale-demo.herokuapp.com/scale/callback" \
      -d instruction="Draw a tight polygon around every **car** in the image." \
      -d attachment_type=image \
      -d attachment="https://scale.com/static/img/website/index/example-ia-boxes.jpg" \
      -d objects_to_annotate="car" \
      -d objects_to_annotate="suv" \
      -d with_labels=true 
    ```
1. Go to `https://scale-demo.herokuapp.com/scale/task/<task_id>` and replace `<task_id>` with your copied value.
     - Example: https://scale-demo.herokuapp.com/scale/task/5e37128484877700100c4e90

### Setting up your own S3 callback server

I wrote this demo so that anyone can clone this repo and set up their own Heroku callback server.  The following steps detail how you can get up and running.  Note, these steps assume you have familiarity with git, GitHub, Heroku, python, AWS console, and the Scale API docs.  This project uses Python 3.6.0.

1. Sign up or log into your Scale dashboard at https://scale.com/ and make sure you have access to your api keys (test and/or live). 

1. Sign up or log into your Heroku dashboard at https://dashboard.heroku.com/apps and make sure you have the Heroku CLI installed https://devcenter.heroku.com/articles/heroku-cli#download-and-install.

1. Sign up or log into your AWS browser console at https://aws.amazon.com/console/:

    - You can either create a new s3 bucket or use an existing one, and you can choose the default configuration options and permissions https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html  
    
    
    - In the browser console under your username in the top nav, click "My security credentials".  You will get a pop-up that says you are acessing security credentials that provide unlimited access to your AWS resources and suggests using IAM access instead.  If you are a wizard in AWS IAM credentials, feel free to PR this repo with better instructions.  This AWS credential setup is only recommended for small tinkering apps.  Keeping this in mind, we will create an access key ID and secret access key pair and will take extra caution to set local environment variables only and never push these credentials to GitHub.

1. Fork this repo and clone into your local workspace: https://github.com/jbarth04/Scale

1. Set up a virtual envrionment `virtualenv` in the local git directory you'll be working installed via `pip`, instructions: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/.  Although this step isn't absolutely necessary, it is highly recommended for a few reasons:

    - You can isolate your run environment to use specific versions of dependencies without having to worry about breaking dependenices of any existing projects
    
    - We will set app specific environment variables and these will also be isolated from your global configs
    
1. Make sure your virtual environment is activate (e.g. `$source <my_virtualenv>/bin/activate`), and then install the required runtime dependenices via:

    `$ pip install -r requirements.txt`
    
1. Now let's setup up our environment variables needed to run our server [scale.py](https://github.com/jbarth04/Scale/blob/master/scale.py).  You will need access to your AWS accessKeyId, AWS secretKey, AWS bucket name, and AWS bucket region (e.g. `us-east-1`). 

    ```
    export S3_ACCESS_KEY="your_s3_access_key"
    export S3_SECRET_KEY="your_s3_secret_key"
    export S3_REGION="your_s3_region"
    export S3_BUCKET_NAME="your_s3_bucket_name"
    ```
    
1. While we're here, let's also set an environment variable to run our script [ScalePolygonAnnotation.py](https://github.com/jbarth04/Scale/blob/master/ScalePolygonAnnotation.py) for testing.

    ```
    export SCALE_API_KEY="your_scale_api_key"
    ```
    
1. Now we want to run our server locally.  This demo uses Flask, which you can read more about here https://flask.palletsprojects.com/en/1.1.x/quickstart/

    ```
    $ export FLASK_APP=scale.py
    $ flask run
    * Running on http://127.0.0.1:5000/
    ```

1. We'll need to actually deploy our server to Heroku to verify the callback gets hits correctly by Scale, but the index page should work.

1. Assuming you can already log into your Heroku Dashboard and have the CLI installed, you can follow these instructions https://devcenter.heroku.com/articles/git

    - Note, if you want you specify you own app name, instead of running `$ heroku create`, run `$ heroku apps:create my-unique-app-name`, docs here https://devcenter.heroku.com/articles/heroku-cli-commands
    
1. Go to your Heroku dashboard and click on your app.  In the `Settings` tab, you'll want to click `Reveal Configs Var` and add your AWS accessKeyId, AWS secretKey, AWS bucket name, and AWS bucket region as key/value pairs, similar to how we exported those configs in our local env.

1. At this point, we assume that you've deployed your app via  `$ git push heroku master` and now we'll get one instance of the app running, docs https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app.  There's a couple things happeneing here:

    - First, we've already defined and deployed our [Procfile](https://github.com/jbarth04/Scale/blob/master/Procfile), which defines the commands that are executed when an instance of our app is spun up, docs https://devcenter.heroku.com/articles/procfile
    
    - We're using Gunicorn, a Python Web Server Gateway Interface HTTP server, to deploy and run our Flask app, docs https://devcenter.heroku.com/articles/procfile
    
    - When we run, `$ heroku ps:scale web=1` it's spinning up a new instance of our app via Gunicorn as specified in our Procfile
    
1. At this point, you should be able to change the `callback_url` in [ScalePolygonAnnotation.py](https://github.com/jbarth04/Scale/blob/master/ScalePolygonAnnotation.py#L9) from `'callback_url': 'https://scale-demo.herokuapp.com/scale/callback'` to the URL of your own app: `'callback_url': 'https://<your-app>.herokuapp.com/scale/callback'`

1. Locally, run `$ python3 ScalePolygonAnnotation.py`.  You'll get a response in the format `{'task_id': '123456789'}`.  Copy the `task_id` value.  Then go to `https://<your-app>.herokuapp.com/scale/task/<task_id>` and verify you can fetch your `task` response from s3.  You should also see in your AWS S3 bucket a corresponding file named after the `<task_id>`.  

1. That's it! Thanks for making it this far.  If there were any steps I missed, please share your debugging woes by opening an issue or email me at josie.barth@gmail.com.
