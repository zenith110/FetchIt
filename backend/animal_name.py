import boto3
import re
import os
import json
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key")
)
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
# Breaks the various species 
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
            if("," in names):
                continue
            else:
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
with open('animal_list.json', 'w') as outfile:
    json.dump(species_names_dict, outfile)