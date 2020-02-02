import requests
import json
import os

def main():
    print("Starting Scale polygon annotation with S3 callback")

    payload = {
        'callback_url': 'https://scale-demo.herokuapp.com/scale/callback',
        'objects_to_annotate': ['car', 'suv'],
        'attachment': 'https://scale.com/static/img/website/index/example-ia-boxes.jpg',
        'with_labels': True,
        'instruction': 'Draw a tight polygon around every **car** in the image.',
        'attachment_type': 'image'
    }

    headers = {"Content-Type": "application/json"}

    task_request = requests.post("https://api.scale.com/v1/task/polygonannotation",
        json=payload,
        headers=headers,
        auth=(os.environ['SCALE_API_KEY'], '')
    )

    print(task_request)

if __name__ == "__main__":
    main()