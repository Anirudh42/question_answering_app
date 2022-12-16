from flask import Flask, request, render_template
from transformers import pipeline
import json, pickle
from gensim.utils import tokenize


app = Flask(__name__)

#Preparing the pretrained QA model
print("Loading the QA model...")
my_context = []
#read the contents of the text file to set the context for the QA model
with open('./data/my_context.txt', encoding="utf8") as f:
    for line in f.readlines():
        my_context.append(line.replace("\n", ""))


full_text = ' '.join(my_context)
qa_model = pipeline("question-answering")
#Preparing the pretrained Sentiment Analysis Model
print("Loading the Sentiment Analysis model...")

#load the vectorizer for the above ML model
with open('ml_model/featurizer.pk', 'rb') as f:
    vectorizer = pickle.load(f)

#load the sentiment analysis ML model
with open('ml_model/sentiment_model.pk', 'rb') as f:
    sentiment_predictor = pickle.load(f)

@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"

@app.route("/sentiment",methods=["GET","POST"])
def predict_sentiment():
    if request.method=="POST":
        input_text = request.form['userinput']
        cleaned_text = [' '.join(list(tokenize(input_text, lowercase=True)))]
        vectorized_text = vectorizer.transform(cleaned_text)
        prediction = sentiment_predictor.predict(vectorized_text)[0]
        response = ["Text": input_text, "Sentiment": "Positive" if prediction = 1 else "Negative"]
        return render_template("user_input.html", data=response)
    return render_template("user_input.html", data=())

@app.route("/qa",methods=["GET","POST"])
def answer_question():
    if request.method=="POST":
        question = request.form['userinput']
        answer = qa_model(question = question, context = my_context)
        response = ["Question": question, "Response": answer]
        response['Answer']['score'] = round(response['Answer']['score']*100,2)
        # response = json.dumps(response, sort_keys = True, indent = 4, separators = (',', ': '))
        return render_template("user_input.html", data=response)
    
    return render_template("user_input.html", data=())
    


if __name__=="__main__":
    app.run(
        host="127.0.0.1", port=5000, debug = True)