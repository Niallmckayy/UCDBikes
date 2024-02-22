import pandas as pd
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template

df = pd.read_json("dublin.json")
def func(df,x):
    try:
        return str(df[df['number'] == x].to_string(header=None,index=False))
    except:
        return "Error"
    
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>asd</h1>"

@app.route('/index/<number>')
def hello(number):
    return render_template('index.html',data = func(df,int(number)), station_number = number)


if __name__ == "__main__":
    app.run(debug=True)