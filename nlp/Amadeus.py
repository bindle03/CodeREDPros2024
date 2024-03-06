import requests
from nlp.converter import *
from nlp.prompt_to_json import *
from nlp.conversation import *

class FieldException(Exception):
    def __init__(self, data):
        self.data = data

class AmadeusException(Exception):
    pass

async def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = f"grant_type=client_credentials&client_id=4Cz3Xv8iQ4o4yl3LpGxXQqMbADgvt3E7&client_secret=tK1jdQ2N4JpdV8fR"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['access_token']

def get_flight_url(departure_city, destination_city, departure_date, adults = 1, children = 0, infants = 0, return_date = None, non_stop = False):
    departure_id_array = city_converter(departure_city)

    destination_id_array = city_converter(destination_city)
    departure_date = date_format(departure_date)
    if (return_date): return_date = date_format(return_date)

    url_array = []
    for departure_id in departure_id_array:
        for destination_id in destination_id_array:
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure_id}&destinationLocationCode={destination_id}&departureDate={departure_date}&adults={adults}&currencyCode=USD&max=5"
            if (return_date): url += f"&returnDate={return_date}"
            if (children): url += f"&children={children}"
            if (infants): url += f"&infants={infants}"
            if (non_stop): url += f"&nonStop=true"

            url_array.append(url)

    return url_array

async def get_best_flights(user_input, chat_history = []):

    headers_flight = {"Authorization" : "Bearer " + await get_token()}

    user_data = extract_to_json(user_input)

    if (not user_data.get('departure_date', None) or not user_data.get('departure', None) or not user_data.get('destination', None)):
        raise FieldException(get_chat_output(json.dumps(user_data), chat_history))

    req_url_array = get_flight_url(user_data['departure'], user_data['destination'], user_data['departure_date'], user_data.get('adults', 1), user_data.get('children', 0), user_data.get('infants', 0), user_data.get('return_date', None), user_data.get('non_stop', False))

    best_flights_all = []

    print(req_url_array)

    for req_url in req_url_array:
        response_flight = requests.get(req_url, headers=headers_flight)

        
        if 'data' in response_flight.json():
            best_flights_all += response_flight.json()['data']
        else:
            raise AmadeusException(response_flight.get('details', 'Unknown error'))


    return {
        "requests": user_data,
        "best_flights": best_flights_all
    }
