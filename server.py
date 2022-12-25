from flask import Flask, request, render_template
from transformers import pipeline
import json, pickle
from gensim.utils import tokenize


app = Flask(__name__)    # __name__ means this current file.

#Preparing the pretrained QA model
print("Loading the QA model...")
my_context = []

#'read the contents of the text file to set the context for the QA model'
with open(".\data\my_context.txt", encoding="utf8") as f:
    for line in f.readlines():
        my_context.append(line.replace('\n','')) # this is for house keeping and cleaning the text clean.
full_text = ' '.join(my_context)

qa_model = pipeline("question-answering") #'initialize the QA model'
#Preparing the pretrained Sentiment Analysis Model
print("Loading the Sentiment Analysis model...")
#'load the sentiment analysis ML model'
with open("./ml_model/sentiment_model.pk",'rb') as f:
    sentiment_model= pickle.load(f)    
#'load the vectorizer for the above ML model' # featurizer convert text to numbers (hot-encode)
with open("./ml_model/featurizer.pk",'rb') as f:
    vectorizer= pickle.load(f)

@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"

@app.route("/sentiment",methods=["GET","POST"])
def predict_sentiment():
    if request.method=="POST":
        #'Get input from web interface'
        input_text = request.form['userinput'] 
        #'perform some basic text cleaning'
        cleaned_text = [' '.join(list(tokenize(input_text,lowercase=True)))] 
        #'convert text into numbers'
        vectorized_text = vectorizer.transform(cleaned_text) 
        #'use the ML model to make a prediction on the sentiment'
        prediction = sentiment_model.predict(vectorized_text)[0] 
        #'formulate the response as a JSON object'
        response = {'Text':input_text,'Sentiment':'Positive' if prediction==1 else 'Negative'}
        #'display result and render on screen'
        return render_template('user_input.html',data=response)
    return render_template('user_input.html',data={}) #'render the html file'

@app.route("/qa",methods=["GET","POST"])
def answer_question():
    if request.method=="POST":
        #'Get input from web interface'
        question =request.form['userinput'] 
        #'get the answer from the QA model'
        answer = qa_model(question=question, context=full_text)
        #'formulate the response as a JSON object'
        response = {"Context":full_text,"Question":question,"Answer":answer}
        response['Answer']['score'] = round(response['Answer']['score']*100,2)
        print(response)
        # response = json.dumps(response, sort_keys = True, indent = 4, separators = (',', ': '))
        return render_template('user_input.html', data=response) #'display result and render on screen'
    
    return render_template('user_input.html', data={})  #'render the html file'


if __name__=="__main__":
 app.run(host="127.0.0.1",port=5000,debug=True) #'command to run the Flask application here'

# Having debug=True allows possible Python errors to appear on the web page. This will help us trace the errors.


