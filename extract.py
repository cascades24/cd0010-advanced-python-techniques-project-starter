"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neo_collection = set()

    #making filename
    #if neo_csv_path[-1] != '/':
    #    filepath = neo_csv_path + '/neos.csv'
    #else:
    #    filepath = neo_csv_path + 'neos.csv'
    #filepath = neo_csv_path + '/neos.csv'
    

    #reading in CSV file
    with open(neo_csv_path) as f:
        reader = csv.reader(f)

        #skipping header line
        next(reader)

        #iterating through the list
        for line in reader:
            neo_collection.add(NearEarthObject(designation=line[3],name=line[4],diameter=line[15],hazardous=line[7],approaches=''))

    # Done: Load NEO data from the given CSV file.
    return (neo_collection)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cad_collection = set()

    #making filename
    #if cad_json_path[-1] != '/':
    #    filepath = cad_json_path + '/cad.json'
    #else:
    #    filepath = cad_json_path + 'cad.json'
    #filepath = cad_json_path + '/cad.json'
    #filepath = cad_json_path
    
    #loading filename
    with open (cad_json_path, 'r') as f:
        cad_data = json.load(f)

    #putting data into set
    for line in cad_data['data']:
        cad_collection.add(CloseApproach(designation=line[0],time=line[3],distance=line[4],velocity=line[7],neo=None))
    

    # Done: Load close approach data from the given JSON file.
    return (cad_collection)

#test code
#load_approaches('/Users/natelee/Documents/cd0010-advanced-python-techniques-project-starter/data/')