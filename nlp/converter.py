import json
from urllib.parse import quote
from dateutil import parser
import string


def date_format(date_string):

    return parser.parse(date_string).strftime("%Y-%m-%d")

def city_converter(city_name):
    city_name = string.capwords(city_name)
    with open("nlp/data/airports.json", "r") as read_file:
        ap_data = json.load(read_file)
            
        iata_codes = []
        for i in ap_data:
            if i["city"] == city_name:
                iata_codes.append(i["iata_code"])

        return iata_codes
