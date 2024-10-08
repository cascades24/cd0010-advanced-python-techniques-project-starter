"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    #defining empty set to store the NEO data
    neo_collection = set()

    #reading in CSV file
    with open(neo_csv_path) as f:
        reader = csv.reader(f)

        #skipping header line
        next(reader)

        #iterating through the list
        for line in reader:
            neo_collection.add(NearEarthObject(designation=line[3],name=line[4],
                                diameter=line[15],hazardous=line[7],approaches=''))

    #returning neo collection
    return (neo_collection)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    #creating empty set for close approach data 
    cad_collection = set()

    #loading filename
    with open (cad_json_path, 'r') as f:
        cad_data = json.load(f)

    #putting data into set
    for line in cad_data['data']:
        cad_collection.add(CloseApproach(designation=line[0],time=line[3],
                            distance=line[4],velocity=line[7],neo=None))
    
    #returning object collection
    return (cad_collection)
