from flask import Flask, request, render_template
# from transformers import pipeline
import json, pickle
from gensim.utils import tokenize


app = Flask(__name__)

#Preparing the pretrained QA model
# print("Loading the QA model...")
# my_context = []
# #Open the file, read every line in the file and append it to a list and make sure there are no '\n' 
# with open("./data/my_context.txt",encoding="utf8") as f:
#     for line in f.readlines():
#         my_context.append(line.replace("\n",""))

# full_text = ' '.join(my_context)
# qa_model = pipeline("question-answering") #initialize the qa model
#Preparing the pretrained Sentiment Analysis Model
print("Loading the Sentiment Analysis model...")
with open("ml_model/sentiment_model.pk",'rb') as f:
    sentiment_predictor = pickle.load(f)
with open("ml_model/featurizer.pk",'rb') as f:
    vectorizer = pickle.load(f)

@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"

@app.route("/sentiment",methods=["GET","POST"])
def predict_sentiment():
    if request.method=="POST":
        input_text = request.form['userinput']
        cleaned_text = [' '.join(list(tokenize(input_text,lowercase=True)))]
        vectorized_text = vectorizer.transform(cleaned_text)
        prediction = sentiment_predictor.predict(vectorized_text)[0]
        response = {"Text":input_text,"Sentiment":"Positive" if prediction==1 else "Negative"}
        return render_template("user_input.html",data=response)
    return render_template("user_input.html",data={})

@app.route("/qa",methods=["GET","POST"])
def answer_question():
    if request.method=="POST":
        question = 'Get input from web interface'
        answer = 'get the answer from the QA model'
        response = 'formulate the response as a JSON object'
        # response['Answer']['score'] = round(response['Answer']['score']*100,2)
        # response = json.dumps(response, sort_keys = True, indent = 4, separators = (',', ': '))
        return 'WIP'
    
    return 'WIP'


if __name__=="__main__":
    app.run(
        host="0.0.0.0",port=5000,debug=True
    )