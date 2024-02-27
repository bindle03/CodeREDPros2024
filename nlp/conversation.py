import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
from dotenv import dotenv_values

config = dotenv_values(".env") | dotenv_values("../.env")

os.environ["OPENAI_API_KEY"] = config["OPEN_API"]


def get_chat_output(query, chat_history = []):

  loader1 = TextLoader("nlp/data/ChatBot.txt")

  #   loader = DirectoryLoader("data/")

  index1 = VectorstoreIndexCreator().from_loaders([loader1])
  

  chain1 = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index1.vectorstore.as_retriever(search_kwargs={"k": 1}),
  )
  
  result = chain1({"question": query, 'chat_history': chat_history})
  chat_history.append((query, result['answer']))
  return {
    'question': query,
    'answer': result['answer'],
    'chat_history': result['chat_history']
  }

def get_new_input(query, chat_history = []):
  loader2 = TextLoader("nlp/data/InputConstructor.txt")

  index2 = VectorstoreIndexCreator().from_loaders([loader2])

  chain2 = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index2.vectorstore.as_retriever(search_kwargs={"k": 1}),
  )

  input = ""

  for (question, answer) in chat_history:
    input += "User: " + question + "\nAssistant: " + answer + "\n"

  input += "User: " + query

  result = chain2({"question": input, 'chat_history': []})
  return result['answer']

# print(get_chat_output("{'destination': 'New York', 'departure_date': '2024-03-08', 'travellers': 3}"))

# print(get_new_input("Atlanta", [("{'destination': 'New York', 'departure_date': '2024-03-08', 'travellers': 3}", "I see you've provided the destination, departure date, and number of travelers. Just a friendly reminder, the departure location is also required to find the best flight offers. Could you please provide the departure location as well? Thank you!")]))

# chat_history = []
# while True:
#   if not query:
#     query = input("Prompt: ")
#   if query in ['quit', 'q', 'exit']:
#     sys.exit()
#   result = chain({"question": query, "chat_history": chat_history})
#   print(result['answer'])

#   chat_history.append((query, result['answer']))
#   query = None