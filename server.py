from flask import Flask
from transformers import pipeline
import json


app = Flask(__name__)
my_context = []
with open("./data/my_context.txt",encoding="utf8") as f:
    for line in f.readlines():
        my_context.append(line.replace("\n",""))

full_text = ' '.join(my_context)
qa_model = pipeline("question-answering")


@app.route("/")
def welcome():
    return "Welcome Brave Warriors! Learn about Game of Thrones by asking questions"


@app.route("/qa",methods=["GET","POST"])
def answer_question():
    question1 = "What is Westeros?"
    question2 = "Who is Night's watch?"
    context = full_text
    answer1 = qa_model(question = question1, context = context)
    answer2 = qa_model(question = question2, context = context)
    response = [{"Question:":question1,"Answer:":answer1},{"Question:":question2,"Answer:":answer2}]
    return json.dumps(response)


if __name__=="__main__":
    app.run(port=5000,debug=True)