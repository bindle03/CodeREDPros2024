import json
from openai import OpenAI
from urllib.parse import quote
from dateutil import parser
import requests
import string
import datetime


def get_city_url(city_name):
    url_encode = quote(city_name)
    
    return f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={url_encode}&page%5Blimit%5D=10&page%5Boffset%5D=0&sort=analytics.travelers.score&view=FULL"

def date_format(date_string):

    print(date_string, flush=True)
    
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
