# nearby restaurant information MOCK
USER_LOCATION = "Cornell Tech"
USER_ZIPCODE = "10044"

# Restaurants
Restaurants = [
    "The Cafe", 
    "Anything At All", 
    "Granny Annies", 
    "Piccolo", 
    "Fuji East",
    "Starbucks", 
    "Subway",
    "Wholesome Factory",
    "NISI",
    "Zhongzhong Noodles"
]

# Descriptions
Descriptions = {
    "The Cafe": "The Cafe",
    "Anything At All": "The restaurant at graduate hotel",
    "Granny Annies": "A popular restaurant on Roosevelt Island", 
    "Piccolo": "A nice pizza restaurant", 
    "Fuji East": "A Japanese restaurant",
    "Starbucks": "A coffee house",
    "Subway": "A fast food restaurant sells sandwiches",
    "Wholesome Factory": "A food and grocery store",
    "NISI": "A popular restaurant on Roosevelt Island",
    "Zhongzhong Noodles": "A Chinese Restaurant"
}

# Distances
Distances = {
    "The Cafe": " on the Campus ",
    "Anything At All": " on the Campus ",
    "Granny Annies": "0.3 mile away ", 
    "Piccolo": " 0.4 mile away ", 
    "Fuji East": "0.4 mile away",
    "Starbucks": "0.4 mile away",
    "Subway": "0.5 mile away",
    "Wholesome Factory": "0.5 mile away",
    "NISI": "0.6 mile away",
    "Zhongzhong Noodles": "0.6 mile away"
}

# Locations
Locations = {
    "The Cafe": "2 W Loop Rd",
    "Anything At All": "22 N Loop Rd",
    "Granny Annies": "425 Main St", 
    "Piccolo": "455 Main St", 
    "Fuji East": "455 Main St",
    "Starbucks": "455 Main St",
    "Subway": "513 Main St",
    "Wholesome Factory": "530 Main St",
    "NISI": "549 Main St",
    "Zhongzhong Noodles": "568 Main St"
}

Location_Full = {
    "The Cafe": "2 West Loop Road",
    "Anything At All": "22 North Loop Road",
    "Granny Annies": "425 Main Street", 
    "Piccolo": "455 Main Street", 
    "Fuji East": "455 Main Street",
    "Starbucks": "455 Main Street",
    "Subway": "513 Main Street",
    "Wholesome Factory": "530 Main Street",
    "NISI": "549 Main Street",
    "Zhongzhong Noodles": "568 Main Street"
}

def describe(res):
    answer = "it is " 
    if res not in Restaurants:
        return ""
    if Descriptions[res]:
        answer = answer +  Descriptions[res]
    answer += ", " + Distances[res]
    return answer
