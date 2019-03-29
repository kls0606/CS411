#Webapp
import json
from flask import Flask, request, render_template
from flask import jsonify
import os

app = Flask(__name__)


@app.route("/")
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    location=request.form['location']
    term=request.form['term']
    script= "python " + "call.py " + "--term=\"" + term + "\"--location=\""+location+"\""
    os.system(script)
    return call()

@app.route("/call")
def call():
    with open('data.json', 'r') as myfile:
        data=myfile.read()
    my_dict = json.loads(data)
    result=my_dict['businesses']
    iterator=[i for i in range(len(result))]
    columnNames=result[0].keys()
    return render_template('record.html',colnames=columnNames, record=result, index=iterator)


if __name__ == "__main__":
    app.run(debug=True)
