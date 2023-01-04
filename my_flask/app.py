import flask
from flask import Flask,render_template,request

app = Flask(__name__)
inp_data=[]

@app.route('/')
def index():
    title='ML Tester'
    return render_template("text_form.html", title=title)

@app.route('/Results',methods=['POST'])
def Results():
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    bmi = request.form.get('bmi')
    region = request.form.get('region')
    children = request.form.get('children')
    smoker = request.form.get('smoker')
    inp_data.append(f"{name}|{age}|{sex}|{bmi}|{region}|{children}|{smoker}")
    return render_template("Results.html",input_data = inp_data)


@app.route('/index')
def home():
    title='ML Tester'
    return render_template("text_form.html", title=title)