from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import json
import os
import random
app = Flask(__name__, static_url_path='/static')
@app.route("/racoon/", methods =["POST", "GET"])    
def racoon_entry():
    if request.method == "GET":
            racoon = racoon_runner()
            return racoon
   
def racoon_runner():
    Image_Files = [d for d in os.listdir("static/racoon/") if ".jpg" in d]
    final_image = random.choice(Image_Files)
    print(final_image)
    data = {}

    # Creates a primary catagory
    data["Racoon".lower()] = []
    # Create a default JSON structure
    data["Racoon".lower()].append({"Image": final_image}) 
    return json.dumps(data, indent=4, sort_keys=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)