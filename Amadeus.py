import requests
from converter import *
from prompt_to_json import *

def get_flight_url(departure_city, destination_city, departure_date, travellers, return_date = None, baggage_quantity = 1):
    departure_id_array = city_converter(departure_city)

    destination_id_array = city_converter(destination_city)
    departure_date = date_format(departure_date)
    if (return_date): return_date = date_format(return_date)

    url_array = []
    for departure_id in departure_id_array:
        for destination_id in destination_id_array:
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure_id}&destinationLocationCode={destination_id}&departureDate={departure_date}&adults={travellers}&nonStop=false&max=250"
            if (return_date): url += f"&returnDate={return_date}"
            url_array.append(url)

    return url_array

def get_best_flights(user_input):
    token_flight = "91Zh8l0QpgeelbwuGRcyF1CUxNzB"

    headers_flight = {"Authorization" : "Bearer " + token_flight}


    user_data = extract_to_json(user_input)

    if (not user_data['departure_date'] or not user_data['departure'] or not user_data['destination']):
        raise Exception("Error: Required fields not found in the user input")

    req_url_array = get_flight_url(user_data['departure'], user_data['destination'], user_data['departure_date'], user_data.get('travellers', 1))

    best_flights_all = []

    print(req_url_array)

    for req_url in req_url_array:
        response_flight = requests.get(req_url, headers=headers_flight)
        
        if 'data' in response_flight.json():
            best_flights_all += response_flight.json()['data']
        else:
            print(response_flight.json())
            print("Error: 'data' key not found in the response JSON")

    return best_flights_all
