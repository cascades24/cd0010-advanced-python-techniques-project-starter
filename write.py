"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    #defining fieldnames for the first row
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    #Opening CSV writer 
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(fieldnames)


        #iterating through results and putting the info into a row for each result
        for result in results:
            ca_results = result.serialize()
            neo_results = result.neo.serialize()
            row = [ca_results['datetime_utc'], ca_results['distance_au'], ca_results['velocity_km_s'],
                   neo_results['designation'], neo_results['name'], 
                   neo_results['diameter_km'], neo_results['potentially_hazardous']]
            csvwriter.writerow(row)   

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    #opening JSON writer and using the .serialize method to pass info
    with open(filename, 'w') as outfile:

        #creating the list to dump the results to the JSON file
        json_list = []
        for result in results:
            json_list.append(result.serialize())
    
    
        json.dump(json_list, outfile, indent=4)
    