from flask import Flask, request, render_template
from transformers import pipeline
#import json, pickle
#from gensim.utils import tokenize
from pysentimiento import create_analyzer


app = Flask(__name__)

#Preparing the pretrained QA model
print("Loading the QA model...")
my_context = []
with open("./data/my_context.txt",encoding="utf8") as f:
    for line in f.readlines():
        my_context.append(line.replace("\n",""))
#'read the contents of the text file to set the context for the QA model'

full_text = ' '.join(my_context)
#'initialize the QA model'
qa_model = pipeline("question-answering")
#Preparing the pretrained Sentiment Analysis Model
print("Loading the Sentiment Analysis model...")
analyzer = create_analyzer(task="sentiment", lang="en")
#'load the sentiment analysis ML model'
#with open('ml_model/sentiment_model.pk','rb') as f:
    #sentiment_predictor = pickle.load(f)
#'load the vectorizer for the above ML model'
#with open('ml_model/featurizer.pk','rb') as f:
#    vectorizer = pickle.load(f)
@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"

@app.route("/sentiment",methods=["GET","POST"])
def predict_sentiment():
    if request.method=="POST":
        input_text = request.form['userinput']  #'Get input from web interface'
        prediction = analyzer.predict(input_text)
        #cleaned_text = [' '.join(list(tokenize(input_text,lowercase=True)))] #'perform some basic text cleaning'
        #vectorized_text = vectorizer.transform(cleaned_text)  #'convert text into numbers'
        #prediction = sentiment_predictor.predict(vectorized_text)[0] #'use the ML model to make a prediction on the sentiment'
        output = prediction.output
        #response = {"Text":input_text,"Sentiment":"Positive" if prediction==1 else "Negative"} #'formulate the response as a JSON object'
        response = {"Text": input_text, "Sentiment": output }
        return render_template("user_input.html",data=response) # 'display result and render on screen'
    return render_template("user_input.html",data={})

@app.route("/qa",methods=["GET","POST"])
def answer_question():
    if request.method=="POST":
        question = request.form['userinput']  #'Get input from web interface'
        answer = qa_model(question = question, context = full_text) #'get the answer from the QA model'
        response = {"Context":full_text,"Question":question,"Answer":answer} #'formulate the response as a JSON object'
        response['Answer']['score'] = round(response['Answer']['score']*100,2)
        print(response)
        # response = json.dumps(response, sort_keys = True, indent = 4, separators = (',', ': '))
        return render_template("user_input.html",data=response) #'display result and render on screen'
    
    return render_template("user_input.html",data={}) #'render the html file'


if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
#    'command to run the Flask application here'
