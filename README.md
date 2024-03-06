# CodeREDPros2024

<img src="https://https://github.com/bindle03/CodeREDPros2024/blob/main/vpt-gallery.jpg" width="500" height="500">

# What It Does
- Create an airline chatbox that when the users type in their cirtiria, it going to look up the suitable flight for them.
- Extract users' input to JSON file using OpenAI.
- Insert the JSON file to Amadeus API to generate the matching results to another JSON file.
- Use OpenAI to convert the result JSON file back to NLP and output the answer to the users.

# Look At Our Project Now
- Devpost: https://devpost.com/software/vpt-nlp-for-flight-booking
- Demo: https://www.youtube.com/watch?v=fDNwpJHFoFQ&feature=youtu.be
- Our app on Google Cloud Platform: coderedpros2024-kxh4l6ww2a-uc.a.run.app (Still limited, slow response)
- Presentation of our project: https://docs.google.com/presentation/d/1n8TVsf2uRkuM_XLk6rV68kIzo7Ub7rWpxZhKvM_UQb0/edit#slide=id.p1

# Tools of Developments
- Front-end: HTML/CSS.
- Back-end: Flask (Python).
- APIs: OpenAI, Amadeus.

# Pipeline of Our Project


# Challenges
- Convert the input cities to their airport code.
- Convert the different input dates to a uniform format.
- Handle the front-end input to make an understandable JSON file in the back-end for further generation.

# Accomplishments
- Create a functioning chatbox website with appealing UI
- Manage large flights dataset in order to give an appropriate response.
- Implement a feature that transfer speech to text input.

# How to use the program
- Clone the project by 
```bash
git clone https://github.com/bindle03/CodeREDPros2024.git
cd CodeREDPros2024
```
- Install the dependencies
```bash
pip install -r requirements.txt # May need to install the C++ build tools
```
- Create a .env file
```python
OPEN_API= # Your OpenAI API key
```
- To run the project
```python
python app.py # The app should be running on port 5000
```
