from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from dotenv import dotenv_values

import datetime

config = dotenv_values(".env") | dotenv_values("../.env")

schema = {
    "properties": {
        "departure": {
            "type": "string", 
            "description": "The name of the city that the user is departing from, leave out if not provided"
        },
        "destination": {
            "type": "string", 
            "description": "This name of the city that the user is travelling to, leave out if not provided"
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
            "type": "integer", "description": "The number of adults travelling with you, if not specified it will be assumed to be 1."
        },
        "children": {
            "type": "integer", "description": "The number of children travelling with you"
        }
    },
}



def extract_to_json(userInput) -> dict[str, any]:


    # class Properties(BaseModel):

    #     departure_name: str
    #     destination_name: str
    #     departure_date: Optional[str]
    #     return_date: Optional[str]

    print("Extracting to JSON...", flush=True)
    chain = create_extraction_chain(schema, llm=ChatOpenAI(openai_api_key=config['OPEN_API'], model="gpt-3.5-turbo"))

    try:
        res = chain.invoke(userInput)
    except Exception as e:
        print(e, flush=True)

    if (type(res['text']) == list) : return res['text'][0]

    print(res['text'], flush=True)

    return res['text']
