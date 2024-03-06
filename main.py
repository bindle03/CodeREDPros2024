# app/routes.py
from flask import Flask, render_template, jsonify, request, session
from nlp.Amadeus import *
import dotenv

import os

app = Flask(__name__)
app.secret_key = 'secret'

config = dotenv.dotenv_values()

@app.route('/')
def home():
    session.clear()

    return render_template('index.html', message='This is a message')

@app.route('/send', methods=['POST'])
async def send():
    input = json.loads(request.data)['inputText']
    chat_history = session.get('chat_history', [])

    input = get_new_input(input, chat_history)
    print("NEW INPUT", input, flush=True)

    try:
        processed = await get_best_flights(input, chat_history)
    except FieldException as e:
        # print("Field exception", e, flush=True)

        session['chat_history'] = e.data.get('chat_history')

        print('HISTORY', chat_history, flush=True)

        return jsonify({
            'missing': True,
            'message': e.data.get('answer')
        })

    print(session.get('chat_history'), flush=True)
    session.clear()

    best_flights = processed['best_flights']

    print(len(best_flights), flush=True)

    if not len(best_flights):
        return {
            'missing': True,
            'message': "Seems like I can not find any flights from my database for your request. Can you try a different place?"
        }
    best_flights = sorted(best_flights, key=lambda x: float(x['price']['grandTotal']))


    # Sort the best_flights by price
    return jsonify({
        'ok': True,
        'missing': False,
        'best_flights': best_flights[:10],
        'requests': processed['requests']
    })

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5000), host='0.0.0.0')