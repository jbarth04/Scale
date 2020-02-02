# ScaleAPI Demo

## Preface
In browsing the Scale API docs, I noticed that the python sample callback server implementation is still in the works (as of Feb 2nd, 2020), https://scale.com/docs?python#callbacks.  I decided it would be a fun exercise to set up an example callback server with a `POST` endpoint that consumes the result of a Scale task and writes it to Amazon S3.

## A simple python callback server for Scale API tasks

This demo project includes the server code [scale.py](https://github.com/jbarth04/Scale/blob/master/scale.py) that is running live on Heroku at https://scale-demo.herokuapp.com/.  You hit the callback server and verify it works by following these steps:

1. Take a sample request from Scale API docs https://scale.com/docs?python#introduction and set the callback to `https://scale-demo.herokuapp.com/scale/callback`.  Examples below: 

    - Clone this repo, set `export SCALE_API_KEY="your_scale_api_key"` in your local env, and run the python script [ScalePolygonAnnotation.py](https://github.com/jbarth04/Scale/blob/master/ScalePolygonAnnotation.py).  You'll get a response in the format `{'task_id': '123456789'}`.  Copy the `task_id` value.
    
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

I wrote this demo so that anyone can clone this repo and set up their own Heroku callback server.  The following steps detail how you can get up and running.  Note, this project uses Python 3.6.0
