# ScaleAPI Demo

## Preface
In browsing the Scale API docs, I noticed that the python sample callback server implementation is still in the works (as of Feb 2nd, 2020), https://scale.com/docs?python#callbacks.  I decided it would be a fun exercise to set up an example callback server with a `POST` endpoint that consumes the result of a Scale task and writes it to Amazon S3.

## A simple python callback server for Scale API tasks

This demo project includes the server code [scale.py](https://github.com/jbarth04/Scale/blob/master/scale.py) that is running live on Heroku at https://scale-demo.herokuapp.com/.  You hit the callback server by:

1) Cloning this repo and run the sample script [ScalePolygonAnnotation](https://github.com/jbarth04/Scale/blob/master/ScalePolygonAnnotation.py) that hits the Scale API with a callback to write to our server, which writes to s3. More examples at https://github.com/scaleapi/scaleapi-python-client

2) Running this cURL command

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

I wrote this demo so that anyone can clone this repo and set up their own Heroku callback server.  See the following instructions.

### Setting up your own S3 callback server

Note, this project uses Python 3.6.0
