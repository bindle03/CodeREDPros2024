from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from dotenv import dotenv_values

import datetime

config = dotenv_values(".env") | dotenv_values("../.env")

schema = {
    "properties": {
        "departure": {
            "type": "string", 
            "description": "The name of the city that the user is departing from make sure that it is a valid city, leave out if not provided"
        },
        "destination": {
            "type": "string", 
            "description": "This name of the city that the user is travelling to make sure that it is a valid city, leave out if not provided"
        },
        "departure_date": {
            "type": "string", 
            "description": "Today's date is " + str(datetime.date.today()) + " the format should be YYYY-MM-DD, if the date is in the past, leave out. Be aware of seasons time, Spring is from March 20 to June 20, Summer is from June 21 to September 21, Fall is from September 22 to December 20, and Winter is from December 21 to March 19."
        },
        "return_date": {
            "type": "string", 
            "description": "Today's date is " + str(datetime.date.today()) + " the format should be YYYY-MM-DD, if the date is in the past, leave out"
        },
        "baggage_quantity": {
            "type": "integer"
        },
        "adults": {
            "type": "integer", "description": "the number of adult travelers (age 12 or older on date of departure), remmember to account for the prompting user. If not specified, the default value is 1. If specified, this number should be greater than or equal to 1."
        },
        "children": {
            "type": "integer", "description": "the number of child travelers (older than age 2 and younger than age 12 on date of departure) who will each have their own separate seat. If specified, this number should be greater than or equal to 0"
        },
        "infants": {
            "type": "integer", "description": "the number of infant travelers (whose age is less or equal to 2 on date of departure). Infants travel on the lap of an adult traveler, and thus the number of infants must not exceed the number of adults. If specified, this number should be greater than or equal to 0"
        },
        "non_stop": {
            "type": "boolean", "description": "if the user want the fastest flights, this should be true, something like 'urgently' or 'quickly'. Otherwise, the user is open to flights with layovers"
        },
    },
    "required" : ["adults", "children", "infants"],
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
