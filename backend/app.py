from flask import Flask, render_template, request, redirect, jsonify, abort
from flask.json import jsonify
import requests
import json
import os
import random
import boto3
import datetime
import os
from flasgger import Swagger
from flask_cors import CORS
import re
from werkzeug.utils import secure_filename
app = Flask(__name__, static_url_path='/static')
CORS(app)
swagger = Swagger(app)
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key")
)

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

@app.route("/species/allspecies/", methods=["GET"])
def all_species():
    """Fetches all the animals and breeds we have available
    ---
    responses:
        200:
            description: Species/Animal names in JSON
    """
    with open("animal_list.json", "r") as file:
        data = json.load(file)
    
    return jsonify(data)



@app.route("/species/", methods =["GET"])    
def species_entry():
    """Fetches animal data
    Name requires hyphens when using a sub_species with spaces
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
      - name: sub-species
        in: query
        type: string
        required: false
    responses:
        200:
            description: Animal JSON response
        400:
            description: Animal/sub species could not be found
            """
    if request.method == "GET":
            species_name = request.args.get("name")
            species_name = species_name.lower()
            sub_species_name = request.args.get("sub-species")
            species = species_runner(species_name, sub_species_name)
            return species

def species_runner(breed_name, sub_species_name):
    animal = []
    final_list = []
    my_bucket = s3.Bucket("fetchitbucket")
    try:
        if(sub_species_name == "" or sub_species_name is None):
            for object_summary in my_bucket.objects.filter(Prefix=breed_name + "/"):
                animal.append(object_summary.key)
            del animal[0]
            for i in animal:
                final_data = i.replace(breed_name, "https://fetchitbucket.s3.us-east-2.amazonaws.com/" + breed_name)
                final_list.append(final_data)
        else:
            for object_summary in my_bucket.objects.filter(Prefix=breed_name + "/" + sub_species_name):
                animal.append(object_summary.key)
            print(animal)
            del animal[0]
            for i in animal:
                print(i)
                final_data = i.replace(breed_name + "/" + sub_species_name, "https://fetchitbucket.s3.us-east-2.amazonaws.com/" + breed_name + "/" + sub_species_name)
                final_list.append(final_data)

        final_image = random.choice(final_list)
        data = {}

        # Creates a primary catagory
        data["animal"] = []
        # Create a default JSON structure
        data["animal"].append({"Image": final_image}) 
        return json.dumps(data, indent=4, sort_keys=True)
    except:
        return abort(404)


@app.route("/upload/single/", methods=["POST"])
def single_upload():
    content = request.form.to_dict()
    picture = request.files.to_dict()
    picture_file = picture["files[]"]
    animal_name = content["animal"]
    sub_species_name = content["sub_species"]
    if(sub_species_name == ""):
        url = animal_name + "/" + picture_file.filename
        s3.Bucket("fetchitbucket").put_object(Key=url, Body=request.files["files[]"], ACL='public-read')
    else:
        url = animal_name + "/" + sub_species_name + "/" + picture_file.filename
        s3.Bucket("fetchitbucket").put_object(Key=url, Body=request.files["files[]"], ACL='public-read')
    return content

# Allows multiple images to be uploaded
@app.route("/upload/multi/", methods=["POST"])
def multi_upload():
    content = request.form.to_dict()
    picture_data = request.files.getlist("files[]")
    animal_name = content["animal"]
    sub_species_name = content["sub_species"]
    for picture_file in picture_data:
        if(sub_species_name == ""):
            url = animal_name + "/" + picture_file.filename
            s3.Bucket("fetchitbucket").put_object(Key=url, Body=picture_file, ACL='public-read')
        else:
            url = animal_name + "/" + sub_species_name + "/" + picture_file.filename
            s3.Bucket("fetchitbucket").put_object(Key=url, Body=picture_file, ACL='public-read')
    return content
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
        return abort(404)

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
    try:
        with open("src/stacks/" + stack_name +  ".json", encoding="utf8") as json_file:
            data = json.load(json_file)
        return json.dumps(data, indent=4, sort_keys=True)
    except:
        return abort(404)


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
    json_file = random.choice(os.listdir("src/FE/"))
    with open("src/FE/" + json_file) as loop:
        data = json.load(loop)
    return json.dumps(data, indent=4, sort_keys=True)


def exam_runner(exam_name):
    try:
        with open("src/FE/" + exam_name + ".json") as json_file:
            data = json.load(json_file)
        return json.dumps(data, indent=4, sort_keys=True)
    except:
        return abort(404)


if __name__ == '__main__':
    if(os.environ.get("prod") == "False"):
        app.run(host="0.0.0.0", port=5000)
    elif(os.environ.get("prod") == "True"):
        app.run(host="0.0.0.0", port=8080)
