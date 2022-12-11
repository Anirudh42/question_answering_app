from flask import Flask, request, render_template
from transformers import pipeline
import json, pickle
from gensim.utils import tokenize


app = Flask(__name__)

#Preparing the pretrained QA model
print("Loading the QA model...")
my_context = []
'read the contents of the text file to set the context for the QA model'

full_text = ' '.join(my_context)
qa_model = 'initialize the QA model'
#Preparing the pretrained Sentiment Analysis Model
print("Loading the Sentiment Analysis model...")
'load the sentiment analysis ML model'
'load the vectorizer for the above ML model'

@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"

@app.route("/sentiment",methods=["GET","POST"])
def predict_sentiment():
    if request.method=="POST":
        input_text = 'Get input from web interface'
        cleaned_text = 'perform some basic text cleaning'
        vectorized_text = 'convert text into numbers'
        prediction = 'use the ML model to make a prediction on the sentiment'
        response = 'formulate the response as a JSON object'
        return 'display result and render on screen'
    return 'render the html file'

@app.route("/qa",methods=["GET","POST"])
def answer_question():
    if request.method=="POST":
        question = 'Get input from web interface'
        answer = 'get the answer from the QA model'
        response = 'formulate the response as a JSON object'
        response['Answer']['score'] = round(response['Answer']['score']*100,2)
        # response = json.dumps(response, sort_keys = True, indent = 4, separators = (',', ': '))
        return 'display result and render on screen'
    
    return 'render the html file'


if __name__=="__main__":
    'command to run the Flask application here'