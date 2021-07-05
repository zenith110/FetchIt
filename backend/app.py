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

@app.route("/species/allspecies/", methods=["GET"])
def all_species():
    """Fetches all the animals and breeds we have available
    ---
    responses:
        200:
            description: Species/Animal names in JSON
    """
    animals = []
    my_bucket = s3.Bucket("fetchitbucket")
    for my_bucket_object in my_bucket.objects.all():
        if("jpg" in my_bucket_object.key or "JPG" in my_bucket_object.key or "png" in my_bucket_object.key 
            or "PNG" in my_bucket_object.key or ".jpeg" in my_bucket_object.key or "FE/" in my_bucket_object.key):
            continue
        animals.append(my_bucket_object.key)
    sub_species = []
    for breeds in animals:
        for my_bucket_object in my_bucket.objects.all():
            if("FE/" in my_bucket_object.key):
                continue
            
            elif(str(breeds) in my_bucket_object.key):
                sub_species.append(my_bucket_object.key)

    sub_species_names = []

    for species in sub_species:
        if("png" in species or "PNG" in species or "jpg" in species or "JPG" in species or "jpeg" in species or "PNG" in species
            or "jpeg" in species or "JPEG" in species):
            species = species.replace(" ", "-")
            data = species.split("-")
            species_names = data[0]
            if "jpg" in species_names or "png" in species_names:
                re.sub("/^.*jpg$", "", species_names)
                species_names = species_names.split("/")
                if (re.findall("^.*jpg$", species_names[1]) or re.findall("^.*png$", species_names[1]) or  re.findall("^.*JPG$", species_names[1])
                    or re.findall("^.*jpeg$", species_names[1])):
                    del species_names[1]
                else:
                    del species_names[2]
                # Break apart the various strings to rejoin them to make it easier to find
                species_names = "/".join(species_names)
                species_names = species_names.split("/")
                species_names = "/".join(species_names)
                sub_species_names.append(species_names)

    final_species_names = list(set(sub_species_names))

    species_names_dict = {}
    for names in final_species_names:
        if(names not in species_names_dict):
            if("/" in names):
                name_split = names.split("/")
                animal_species = name_split[0]
                sub_species = name_split[1]
                animal_species = animal_species.replace(" ", "_")
                if(animal_species not in species_names_dict):
                    species_names_dict[animal_species] = [sub_species]
                else:
                    species_names_dict[animal_species].append(sub_species)
            else:
                species_include_a_space = names.replace(" ", "_")
                species_names_dict[species_include_a_space] = ""
    print(species_names_dict)

    return jsonify(species_names_dict)



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
    print(content)
    # animal_name = ["animal_name"]
    # sub_species = ["sub_species"]
    # animal_pic = request.files['file']
    # saved_animal_pic = 'static/images/'+str(secure_filename(animal_pic.filename))
    # animal_pic.save(saved_animal_pic)
    # print(saved_animal_pic)
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
