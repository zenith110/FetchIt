from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import json
import os
import random
import boto3
app = Flask(__name__, static_url_path='/static')
with open("settings/aws_role") as loop:
    data = json.load(loop)
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key']
)
@app.route("/racoon/", methods =["POST", "GET"])    
def racoon_entry():
    if request.method == "GET":
            racoon = racoon_runner()
            return racoon
   
def racoon_runner():
    # images = [d for d in s3.Bucket('fetchitbucket').objects.all() if ".jpg" in d]
    # for obj in s3.Bucket('fetchitbucket').Object("racoon/"):
    #     print(obj)
    # Image_Files = [d for d in os.listdir("static/racoon/") if ".jpg" in d]
    racoon = []
    final_list = []
    my_bucket = s3.Bucket("fetchitbucket")
    for object_summary in my_bucket.objects.filter(Prefix="racoon/"):
        racoon.append(object_summary.key)
    del racoon[0]
    for i in racoon:
        final_data = i.replace("racoon", "https://fetchitbucket.s3.us-east-2.amazonaws.com/racoon")
        final_list.append(final_data)

    final_image = random.choice(final_list)
    data = {}

    # Creates a primary catagory
    data["Racoon".lower()] = []
    # Create a default JSON structure
    data["Racoon".lower()].append({"Image": final_image}) 
    return json.dumps(data, indent=4, sort_keys=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)