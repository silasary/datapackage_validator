# pyright: reportTypedDictNotRequiredAccess=false
import sys
import os
import json
import argparse

import worlds

print("\n")

parser = argparse.ArgumentParser(description="Validate data package against known good file")
parser.add_argument("input_file_path", help="Path to the input file")
parser.add_argument("game_name", help="Name of the game")
args = parser.parse_args()

input_file_path = args.input_file_path
game_name = args.game_name

if not os.path.exists(input_file_path):
    parser.error("Path not valid")
with open(input_file_path) as f:
    datapackage_export: worlds.DataPackage = json.load(f)

if game_name not in datapackage_export["games"].keys():
    parser.error("Game name not found in known good file")
if game_name not in worlds.network_data_package["games"].keys():
    parser.error("Game name not found in Archipelago install")

known_datapackage = datapackage_export["games"][game_name]
active_datapackage = worlds.network_data_package["games"][game_name]

discrepencies : dict[str, dict[str,dict]] = {}

def validate_items(known_datapackage, active_datapackage, discrepencies):
    known_good_items = known_datapackage["item_name_to_id"]
    validation_items = active_datapackage["item_name_to_id"]
    # excluded_item_ids = []
    # checked_validation_items = validation_items.keys #list of validation keys, items removed when checking values against known good item list and remaining items are not found in known good items kno


    for item, id in known_good_items.items():
        if not item in validation_items.keys():
            discrepencies[item] = {item : {"type" : "item", "known" : item, "validation" : None}}
        # excluded_item_ids.append(id)
        elif not validation_items[item] == id:
        # checked_validation_items.pop(item)
            discrepencies[item] = {item : {"type" : "id" ,"known" : id, "validation" : validation_items[item]}}
            print(f"{item}: expected id: {id}, found id: {validation_items[item]}")

    # for id in excluded_item_ids:
    #     if id in validation_items.values():
    #         discrepencies[id] = {id  : {"type" : "id reuse", "known" : id in known_good_items}}

    # for item, val in discrepencies.items():

    #     if val["type"] == "id":
    #         print(f"{item}: {"known"} -> {"validation"}")


    # if not len(checked_validation_items) == 0:
    #     for item in checked_validation_items:
    #         discrepencies[item] = {item : {"type" : "item", "known" : None, "validation" : item}}

def validate_locations(known_datapackage, active_datapackage, discrepencies):
    known_good_locations = known_datapackage["location_name_to_id"]
    validation_locations = active_datapackage["location_name_to_id"]
    for location, id in known_good_locations.items():
        if not location in validation_locations.keys():
            discrepencies[location] = {location : {"type" : "location", "known" : location, "validation" : None}}
        # excluded_location_ids.append(id)
        elif not validation_locations[location] == id:
        # checked_validation_locations.pop(location)
            discrepencies[location] = {location : {"type" : "id" ,"known" : id, "validation" : validation_locations[location]}}
            print(f"{location}: expected id: {id}, found id: {validation_locations[location]}")

    # for id in excluded_location_ids:
        # if id in validation_locations.values():
        #     discrepencies[id] = {id  : {"type" : "id reuse", "known" : id in known_good_locations}}

validate_items(known_datapackage, active_datapackage, discrepencies)
validate_locations(known_datapackage, active_datapackage, discrepencies)

if len(discrepencies) == 0:
    print("Validation successful, no discrepencies found")
    sys.exit(0)
else:
    print(f"Validation failed, {len(discrepencies)} discrepencies found")
    sys.exit(1)
