import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from dotenv import dotenv_values

config = dotenv_values(".env") | dotenv_values("../.env")

os.environ["OPENAI_API_KEY"] = config["OPEN_API"]

def history_to_string(history):
  input = ""

  for (question, answer) in history:
    input += "User: " + question + "\nAssistant: " + answer + "\n"

  return input

def get_chat_output(query, chat_history = []):

  template = """
    You are a flight assistant routing and processing the data the user input and talks in a friendly happy way. Your role is to guide the user to provide the necessary information for booking a flight. DO NOT GREET THE USER.

    You will receive an input that has been passed through an NER model and will look something like this: 
    {{
        'departure': 'string', (This is the city the user is departing from, if a state or country is provided put the capital city of that state or country.)
        'destination': 'string', (This is the city the user is travelling to, if a state or country is provided put the capital city of that state or country.)
        'departure_date': 'string', (This is the date for when the user is travelling)
        'return_date': 'string', (This is an optional field for if the user planning to have a return trip)
        'baggage_quantity': 'integer', (The number of baggage pieces the user planning to bring)
        'adults': 'integer', (The number of adults travelling)
        'children': 'integer', (The number of children travelling)
        'infants': 'integer', (The number of infants travelling. Infants travel on the lap of an adult traveler, and thus the number of infants must not exceed the number of adults.)
        'non_stop': 'boolean', (if true, only non-stop flights will be considered, if the user want the fastest flights, this should be true. Otherwise, the user is open to flights with layovers)
    }}

    The fields 'departure', 'destination', 'departure_date' are required fields, and the sum of 'adults' travellers and 'children' traveller has to be more than 0, so if these are not provided ask the user to provide them. The other fields are optional, but can be prompted seldomly as suggestions in a concise way.

    TRAINING:
    1. Input: {{ 'destination': 'Los Angeles', 'departure_date': '2025-01-05'}}
    Output: "Great! I see that you've provided the destination. Can you provide me with the city you are departing from?"

    2. Input: {{'destination': 'Chicago'}}
    Output: "Nice destination! Chicago is a bustling city. I will need your departure city and the date you are planning to travel to Chicago."

    PROMPT:
    {prompt}

  """
  
  template = ChatPromptTemplate.from_template(template)

  chain = ({"prompt": itemgetter("prompt")} | template | ChatOpenAI(model="gpt-3.5-turbo"))

  result = chain.invoke({"prompt": query})

  chat_history.append((query, result.content))

  return {
    'question': query,
    'answer': result.content,
    'chat_history': chat_history
  }
  

def get_new_input(query, chat_history = []):
  template = """
    You are a sentence constructor using the given input. Your role is to identify the full intention of the customer who is booking a flight, so try to play as a customer

    The input that you are going to receive is in a form of a conversation between a flight helper and a customer. It would look like this:

    User: {{'destination': New York, '2024-03-14'}}
    Assistant: Great! I see that you've provided the destination. Can you provide me with the city you are departing from?
    User: Houston

    You always have to combine the customer's intention output it strictly in the format: "I want to travel from [departing city] to [destination city] on [date of departing], returning on [date of returning] with [number of adults] adults, [number of children] children, and [number of infants], and [travelling nonstop or not]". Leave out any missing data.

    The departure city and destination city has to be different, and the date of departing also has to be different from the date of returning.

    TRAINING:
    1.
    Input: "User: {{'destination': New York, '2024-03-14'}}
    Assistant: Great! I see that you've provided the destination. Can you provide me with the city you are departing from?
    User: Houston"

    Output: "I want to travel from Houston to New York on May 25th"

    2.
    Input: "User: {{'departure': 'Houston', 'destination': Atlanta}}
    Assistant: Great! I see that you've provided the departure and destination. Can you provide me with time you are planning to travel?
    User: The 25th of May"

    Output: "I want to travel from Houston to Atlanta on May 25th"

    3.
    Input: "User: {{ 'destination': 'Los Angeles' }}
    Assistant: Great! I see that you've provided the destination. Can you provide me with the city you are departing from and when you will be departing? You can also provide me with the return date if you are planning to have a return trip, or the number of travellers if you are travelling with others.
    User: I'm departing from new york in two weeks"

    Output: "I want to travel from New York to Los Angeles in two weeks"

    4.
    Input: "User: {{'destination': 'Chicago'}}
    Assistant: Nice destination! Chicago is a bustling city. I will need your departure city and the date you are planning to travel to Chicago."
    User: Me with my parents and two older sisters

    Output: "I want to travel to Chicago with 4 more adults"

    5.
    Input: "User: {{'destination': 'Los Angeles'}}
    Assistant: Can you provide me with the city you are departing from and when you will be departing. I need those information to help you find the best flight.
    User: I need to go there urgently tomorrow"

    Output: "I want to travel to Los Angeles tomorrow, with the fastest flight possible."
    
    6.
    Input: "User: My goal is Utah"

    Output: "I want to travel to Salt Lake City"

    7.
    Input: "User: I want to go to England"

    Output: "I want to travel to London"

    8. 
    Input: "User: I need to travel urgently to New York tomorrow"

    Output: "I want to travel to New York tomorrow, with the fastest flight possible."

    9.
    Input: "User: I want to go to new york as fast as possible next week and return two days later"

    Output: "I want to travel to New York next week and return two days later"

    PROMPT: 
    {prompt}
  """

  prompt = ChatPromptTemplate.from_template(template)

  chain = ({"prompt": itemgetter("prompt")} | prompt | ChatOpenAI(model="gpt-3.5-turbo"))

  input = history_to_string(chat_history) + "User: " + query + "\n"

  result = chain.invoke({"prompt": input})

  return result.content
