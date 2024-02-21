# app/routes.py
from flask import Flask, render_template, jsonify, request
from Amadeus import *
from speech_to_text.speech_to_text import *


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', message='This is a message')


@app.route('/send', methods=['POST'])
async def send():
    input = json.loads(request.data)['inputText']

    try:
        best_flights = await get_best_flights(input)
    except Exception as e:
        print("API exception", e, flush=True)

        return jsonify({
            'ok': False,
            'message': "Can you provide more information? I need a departure city, a destination city, and a departure date to find a flight."
        })

    print(len(best_flights), flush=True)

    best_flights = sorted(best_flights, key=lambda x: x['price']['grandTotal'])

    # Sort the best_flights by price
    return jsonify({
        'ok': True,
        'best_flights': best_flights[:10]
    })

if __name__ == '__main__':
    app.run(debug=True)