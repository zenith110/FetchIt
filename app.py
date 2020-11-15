from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import json
import os
import random
import boto3
import subprocess
from discord_webhook import DiscordWebhook, DiscordEmbed
import docker
import dockerhub_login
import datetime
import discord_key
app = Flask(__name__, static_url_path='/static')
with open("src/settings/aws_role.json") as loop:
    data = json.load(loop)
    
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key']
)

@app.route("/update/", methods =["POST", "GET"])
def update_data():
    """
    Does some configuring for dockerhub
    """
    client = docker.from_env()
    client.login(username=dockerhub_login.username, password=dockerhub_login.password)

    """
    If there's a docker instance, pull the latest image from the repo
    """
    down = DiscordWebhook(url=discord_key.api_key, content="FetchIt is going down for a bit!")
    down_response = down.execute()
    try:
        client.images.pull(dockerhub_login.repo)
    # Removes the last instance and pulls the new one
    except:
        client.images.remove(dockerhub_login.repo + ":latest")
        client.images.pull(dockerhub_login.repo)

    # Attempts to deploys a docker container
    try:
        docker_container = client.containers.run(dockerhub_login.repo + ":latest", name= "fetchit")
    # If a docker container exist with the name, remove it and make a new instance
    except:
        fetchit = client.containers.get("fetchit")
        fetchit.stop()
        client.containers.prune()
        subprocess.Popen("sudo", "killall", "app.py")
        now = datetime.now()
        month = datetime.date.today()
        time_stamp = str(now.strftime("%b %d %Y %H:%M:%S"))
        up = DiscordWebhook(url=discord_key.api_key, content='FetchIt is up again! Done at:\n' + time_stamp)
        up_response = up.execute()
        docker_container = client.containers.run(dockerhub_login.repo + ":latest", name= "fetchit")
    return "Now running FetchIt!"

animal_names = ["Fox", "Raccoon", "Chimpanzee", "Lion", "Gorilla", "Hedgehog", "Hamster"]
@app.route("/species/allspecies/", methods = ["POST", "GET"])
def all_species():
    data = []
    for name in animal_names:
        data.append({"name": name})

    return jsonify(data)

@app.route("/species/", methods =["POST", "GET"])    
def species_entry():
    if request.method == "GET":
            species_name = request.args.get("name")
            species_name = species_name.lower()
            species = species_runner(species_name)
            return species

def species_runner(breed_name):
    animal = []
    final_list = []
    my_bucket = s3.Bucket("fetchitbucket")
    try:
        for object_summary in my_bucket.objects.filter(Prefix=breed_name + "/"):
            animal.append(object_summary.key)
        del animal[0]
        for i in animal:
            final_data = i.replace(breed_name, "https://fetchitbucket.s3.us-east-2.amazonaws.com/" + breed_name)
            final_list.append(final_data)

        final_image = random.choice(final_list)
        data = {}

        # Creates a primary catagory
        data["animal"] = []
        # Create a default JSON structure
        data["animal"].append({"Image": final_image}) 
        return json.dumps(data, indent=4, sort_keys=True)
    except:
        return "We don't have that animal, sorry!"


@app.route("/FE/exams/allexams/", methods =["POST", "GET"])
def all_exams():
     # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_exams".lower()] = []
    names = os.listdir("src/FE/")
    # Create a default JSON structure
    for exam_name in names:
        exam_name = exam_name.replace(".json", "")
        data["All_Exams".lower()].append({"Exam": exam_name}) 
    return jsonify(data["All_Exams".lower()])

@app.route("/FE/questions/allstacks/", methods=["POST", "GET"])
def all_stacks():
      # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_Stacks".lower()] = []
    names = os.listdir("src/stacks/")
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
    names = os.listdir("src/dsn/")
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
    json_file = random.choice(os.listdir("src/dsn/"))
    print(json_file)
    with open("src/dsn/" + json_file, encoding="utf8") as loop:
        data = json.load(loop)
    
    return json.dumps(data, indent=4, sort_keys=True)
    
def dsn_runner(dsn_name):
    try:
        with open("src/dsn/" + dsn_name +  ".json", encoding="utf8") as json_file:
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
    json_file = random.choice(os.listdir("src/stacks/"))
    with open("src/stacks/" + json_file, encoding="utf8") as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)
    
def stack_runner(stack_name):
    with open("src/stacks/" + stack_name +  ".json", encoding="utf8") as json_file:
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
    with open("src/FE/" + json_file) as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)
    
def exam_runner(exam_name):
    with open("src/FE/" + exam_name + ".json") as json_file:
        data = json.load(json_file)
    return json.dumps(data, indent=4, sort_keys=True)

@app.route("/", methods =["POST", "GET"])    
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)