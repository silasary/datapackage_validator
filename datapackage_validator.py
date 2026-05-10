# pyright: reportTypedDictNotRequiredAccess=false
import sys
import os
import json
import argparse

import worlds
from NetUtils import GamesPackage


print("\n")
parser = argparse.ArgumentParser(
    description="Validate data package against known good file"
)
parser.add_argument(
    "input_file_path",
    help="Path to the input file",
    default=os.getenv("DATAPACKAGE_EXPORT_PATH"),
    nargs="?",
)
parser.add_argument(
    "game_name",
    help="Name of the game",
    default=os.getenv("DATAPACKAGE_EXPORT_GAME_NAME"),
    nargs="?",
)

parser.add_argument(
    "--update-datapackage",
    action="store_true",
    help="Update the datapackage export if validation is successful",
    default=os.getenv("DATAPACKAGE_EXPORT_UPDATE", "false").lower()
    in ("true", "1", "t"),
)
args = parser.parse_args()

input_file_path = args.input_file_path
game_name = args.game_name
update_datapackage = args.update_datapackage

if input_file_path is None:
    parser.error("Input file path not provided. Provide as argument or set DATAPACKAGE_EXPORT_PATH environment variable")
elif not os.path.exists(input_file_path):
    parser.error("Path not valid")

if game_name is None:
    parser.error("Game name not provided. Provide as argument or set DATAPACKAGE_EXPORT_GAME_NAME environment variable")

with open(input_file_path) as f:
    datapackage_export: worlds.DataPackage = json.load(f)

if game_name not in datapackage_export["games"].keys():
    parser.error("Game name not found in known good file")
if game_name not in worlds.network_data_package["games"].keys():
    parser.error("Game name not found in Archipelago install")

known_datapackage = datapackage_export["games"][game_name]
active_datapackage = worlds.network_data_package["games"][game_name]

discrepancies: list[str] = []


def validate_items(    
    known_datapackage: GamesPackage,
    active_datapackage: GamesPackage,
    discrepancies: list[str],
) -> None:
    known_good_items = known_datapackage["item_name_to_id"]
    validation_items = active_datapackage["item_name_to_id"]
    # excluded_item_ids = []
    # checked_validation_items = validation_items.keys #list of validation keys, items removed when checking values against known good item list and remaining items are not found in known good items kno

    for item, id in known_good_items.items():
        if item not in validation_items.keys():
            discrepancies.append(f"Item Missing from new data: {item}")#{
            #     item: {"type": "item", "known": item, "validation": None}
            # }
        # excluded_item_ids.append(id)
        elif not validation_items[item] == id:
            # checked_validation_items.pop(item)
            discrepancies.append(f"Item id mismatch: {id} -> {validation_items[item]}")#{
            #     item: {"type": "id", "known": id, "validation": validation_items[item]}
            # }
            print(f"{item}: expected id: {id}, found id: {validation_items[item]}")

    # for id in excluded_item_ids:
    #     if id in validation_items.values():
    #         discrepancies[id] = {id  : {"type" : "id reuse", "known" : id in known_good_items}}

    # for item, val in discrepancies.items():

    #     if val["type"] == "id":
    #         print(f"{item}: {"known"} -> {"validation"}")

    # if not len(checked_validation_items) == 0:
    #     for item in checked_validation_items:
    #         discrepancies[item] = {item : {"type" : "item", "known" : None, "validation" : item}}


def validate_locations(
    known_datapackage: GamesPackage,
    active_datapackage: GamesPackage,
    discrepancies: list[str],
) -> None:
    known_good_locations = known_datapackage["location_name_to_id"]
    validation_locations = active_datapackage["location_name_to_id"]
    for location, id in known_good_locations.items():
        if location not in validation_locations.keys():
            discrepancies.append(f"Location Missing from new data: {location}")#{
                #location: {"type": "location", "known": location, "validation": None}
            #}
        # excluded_location_ids.append(id)
        elif not validation_locations[location] == id:
            #checked_validation_locations.pop(location)
            discrepancies.append(f"Location id mismatch: {id} -> {validation_locations[location]}")#{
            #     location: {
            #         "type": "id",
            #         "known": id,
            #         "validation": validation_locations[location],
            #     }
            # }
            print(
                f"{location}: expected id: {id}, found id: {validation_locations[location]}"
            )

    # for id in excluded_location_ids:
    # if id in validation_locations.values():
    #     discrepancies[id] = {id  : {"type" : "id reuse", "known" : id in known_good_locations}}


validate_items(known_datapackage, active_datapackage, discrepancies)
validate_locations(known_datapackage, active_datapackage, discrepancies)

if len(discrepancies) == 0:
    print("Validation successful, no discrepancies found")
    if (
        update_datapackage
        and active_datapackage["checksum"] != known_datapackage["checksum"]
    ):
        print("Updating datapackage export with current datapackage")
        datapackage_export["games"][game_name] = active_datapackage
        with open(input_file_path, "w") as f:
            json.dump(datapackage_export, f, indent=4)
    sys.exit(0)
else:
    print(f"Validation failed, {len(discrepancies)} discrepancies found")
    for dis in discrepancies:
        print(dis)
    sys.exit(1)
