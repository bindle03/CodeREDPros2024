import json
from openai import OpenAI
from typing import Optional, List
from pydantic import Field
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from dotenv import dotenv_values

import datetime

config = dotenv_values(".env") | dotenv_values("../.env")

llm = ChatOpenAI(openai_api_key=config['OPEN_API'], model="gpt-3.5-turbo")

def extract_to_json(userInput) -> dict[str, any]:


    # class Properties(BaseModel):

    #     departure_name: str
    #     destination_name: str
    #     departure_date: Optional[str]
    #     return_date: Optional[str]

    schema = {
        "properties": {
            "departure": {
                "type": "string", 
                "description": "This has to be the city you are departing from, if not provided it will be assumed to be Houston."
            },
            "destination": {
                "type": "string", 
                "description": "This has to be the city you are travelling to, if a country is provided it will be assumed to be the capital city of that country, ex: if England London."
            },
            "departure_date": {
                "type": "string", 
                "description": "Today's date is " + str(datetime.date.today()) + " the format should be YYYY-MM-DD"
            },
            "return_date": {
                "type": "string", 
                "description": "Today's date is " + str(datetime.date.today()) + " the format should be YYYY-MM-DD"
            },
            "baggage_quantity": {
                "type": "integer"
            },
            "adults": {
                "type": "integer", "description": "The number of adults travelling with you, if not specified it will be assumed to be 1, and if the not specified as children it will be assumed to be an adult."
            },
            "children": {
                "type": "integer", "description": "The number of children travelling with you"
            }
        },
        "required": ["departure"],
    }

    
    chain = create_extraction_chain(schema, llm=llm)
    res = chain.invoke(userInput)


    if (type(res['text']) == list) : return res['text'][0]

    print(res['text'], flush=True)

    return res['text']

# print(extract_to_json("I and two adults each has two children want to travel to Spain"))