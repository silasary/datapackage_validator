import sys
import os
import json
import worlds

arg1 = sys.argv[1]
arg2 = sys.argv[2]


#Check if valid arg
if not os.path.exists(arg1):
    raise ValueError("Path not valid")
    sys.exit(-1)
try:
    with open(arg1) as f:
        known_good: worlds.DataPackage = json.load(f)
except TypeError:
    sys.exit(-2)

world_data = worlds.network_data_package["games"][arg2]

known_good_items = known_good["games"][arg2]["item_name_to_id"]
validation_items = world_data["item_name_to_id"]
discrepencies : dict[str, dict[str,dict]] = {}
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


known_good_locations = known_good["games"][arg2]["location_name_to_id"]
validation_locations = world_data["location_name_to_id"] 
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

if len(discrepencies) == 0:
    sys.exit(0)
else:
    sys.exit(1)