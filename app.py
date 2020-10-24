from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import json
import os
import random
import boto3
app = Flask(__name__, static_url_path='/static')
with open("settings/aws_role.json") as loop:
    data = json.load(loop)
    
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key']
)
animal_names = ["Fox", "Raccoon"]
@app.route("/breeds/allbreeds/", methods = ["POST", "GET"])
def allbreeds():
    data = {}
    data["All_Species".lower()] = []
    for name in animal_names:
        data["All_Species".lower()].append({"Name": name}) 
    return json.dumps(data, indent=4, sort_keys=True)

@app.route("/breeds/fox/", methods =["POST", "GET"])    
def fox_entry():
    if request.method == "GET":
            fox = fox_runner()
            return fox

def fox_runner():
    fox = []
    final_list = []
    my_bucket = s3.Bucket("fetchitbucket")
    for object_summary in my_bucket.objects.filter(Prefix="fox/"):
        fox.append(object_summary.key)
    del fox[0]
    for i in fox:
        final_data = i.replace("fox", "https://fetchitbucket.s3.us-east-2.amazonaws.com/fox")
        final_list.append(final_data)

    final_image = random.choice(final_list)
    data = {}

    # Creates a primary catagory
    data["Fox".lower()] = []
    # Create a default JSON structure
    data["Fox".lower()].append({"Image": final_image}) 
    return json.dumps(data, indent=4, sort_keys=True)


@app.route("/breeds/raccoon/", methods =["POST", "GET"])    
def racoon_entry():
    if request.method == "GET":
            racoon = racoon_runner()
            return racoon
   
def racoon_runner():
    raccoon = []
    final_list = []
    my_bucket = s3.Bucket("fetchitbucket")
    for object_summary in my_bucket.objects.filter(Prefix="raccoon/"):
        raccoon.append(object_summary.key)
    del raccoon[0]
    for i in raccoon:
        final_data = i.replace("raccoon", "https://fetchitbucket.s3.us-east-2.amazonaws.com/raccoon")
        final_list.append(final_data)

    final_image = random.choice(final_list)
    data = {}

    # Creates a primary catagory
    data["Raccoon".lower()] = []
    # Create a default JSON structure
    data["Raccoon".lower()].append({"Image": final_image}) 
    return json.dumps(data, indent=4, sort_keys=True)

@app.route("/FE/exams/allexams", methods =["POST", "GET"])
def all_exams():
     # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_exams".lower()] = []
    names = os.listdir("FE/")
    # Create a default JSON structure
    for exam_name in names:
        exam_name = exam_name.replace(".json", "")
        data["All_Exams".lower()].append({"Exam": exam_name}) 
    return jsonify(data["All_Exams".lower()])

@app.route("/FE/questions/allstacks", methods=["POST", "GET"])
def all_stacks():
      # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_Stacks".lower()] = []
    names = os.listdir("stacks/")
    # Create a default JSON structure
    for stack_name in names:
        stack_name = stack_name.replace(".json", "")
        data["All_Stacks".lower()].append({"Stack": stack_name}) 
    return jsonify(data["All_Stacks".lower()])

@app.route("/FE/questions/alldsn/", methods=["POST", "GET"])
def all_dns():
      # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_DSN".lower()] = []
    names = os.listdir("dsn/")
    # Create a default JSON structure
    for dsn_name in names:
        dsn_name = dsn_name.replace(".json", "")
        data["All_DSN".lower()].append({"DSN": dsn_name}) 
    return jsonify(data["All_DSN".lower()])

@app.route("/FE/questions/dsn/", methods =["POST", "GET"])
def dsn():
     if request.method == "GET":
            dsn = request.args.get("name")
            if(dsn == ""):
                dsn = random_dsn()
                return dsn
            else:
                dsn = dsn_runner(dsn)
                return dsn
                
def random_dsn():
    json_file = random.choice(os.listdir("dsn"))
    with open("dsn/" + json_file, encoding="utf8") as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)
    
def dsn_runner(dsn_name):
    try:
        with open("/dsn/" + dsn_name +  ".json", encoding="utf8") as json_file:
            data = json.load(json_file)
        return json.dumps(data, indent=4, sort_keys=True)
    except:
        return "500"

@app.route("/FE/questions/stack/", methods =["POST", "GET"])
def stacks():
     if request.method == "GET":
            stack = request.args.get("name")
            if(stack == ""):
                stack = random_stack()
                return stack
            else:
                stack = stack_runner(stack)
                return stack
                
def random_stack():
    json_file = random.choice(os.listdir("stacks"))
    with open("stacks/" + json_file, encoding="utf8") as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)
    
def stack_runner(stack_name):
    with open("stacks/" + stack_name +  ".json", encoding="utf8") as json_file:
        data = json.load(json_file)
    return json.dumps(data, indent=4, sort_keys=True)

@app.route("/FE/exam/", methods =["POST", "GET"])    
def exam():
    if request.method == "GET":
            exam = request.args.get("name")
            if(exam == ""):
                exam = random_exam()
                return exam
            else:
                exam = exam_runner(exam)
                return exam

def random_exam():
    json_file = random.choice(os.listdir("FE"))
    with open("FE/" + json_file) as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)
    
def exam_runner(exam_name):
    with open("FE/" + exam_name + ".json") as json_file:
        data = json.load(json_file)
    return json.dumps(data, indent=4, sort_keys=True)

@app.route("/", methods =["POST", "GET"])    
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)