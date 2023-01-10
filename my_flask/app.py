# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:50:25 2023

@author: vmadmin
"""

import flask
from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

## Initialize the Database
db=SQLAlchemy(app)

## Create a DB model
class Friends(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(50),primary_key=False)
    Age = db.Column(db.Integer,nullable=False)
    Sex = db.Column(db.String(6),nullable=False)
    Bmi = db.Column(db.Float,nullable=False)
    Region = db.Column(db.String(12),nullable=False)
    Children = db.Column(db.Integer,nullable=False)
    Smoker = db.Column(db.String(4),nullable=False)
    
#    def __init__(self, thewords):
#        self.words = thewords
        
    #Function that will return a string 
    #def __repr__(self):
    #    return '<Names %r' % self.ID

with app.app_context():
    db.create_all()

inp_data=[]

@app.route('/friends')
def friends2():
    title='Data List with Friends'
    return render_template('friends.html', title=title)

@app.route('/')
def index():
    title='ML Tester'
    return render_template("text_form.html", title=title)

"""
@app.route('/Results',methods=['POST','GET'])
def Results():
    if request.method=="POST":
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        bmi = request.form.get('bmi')
        region = request.form.get('region')
        children = request.form.get('children')
        smoker = request.form.get('smoker')

        #return render_template("Results.html", friends=newtestdata)
        inp_data.append(f"{name}|{age}|{sex}|{bmi}|{region}|{children}|{smoker}")
        return render_template("Results.html",input_data = inp_data)
"""
@app.route('/Results',methods=['POST','GET'])
def Results():
    if request.method=="POST":
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        bmi = request.form.get('bmi')
        region = request.form.get('region')
        children = request.form.get('children')
        smoker = request.form.get('smoker')
        pers_age=Friends(Age=age);
        pers_name = Friends(Name=name);
        pers_sex = Friends(Sex=sex);pers_bmi=Friends(Bmi=bmi);
        pers_region = Friends(Region=region);pers_children=Friends(Children=children);
        pers_smoker = Friends(Smoker = smoker)
        
        #return render_template("Results.html", friends=newtestdata)
        inp_data.append(f"{name}|{age}|{sex}|{bmi}|{region}|{children}|{smoker}")
        #return render_template("Results.html",input_data = inp_data)
        
        try:
            #db.session.add(pers_name);db.session.add(pers_age);db.session.add(pers_sex);db.session.add(pers_bmi);db.session.add(pers_region);db.session.add(pers_children);db.session.add(pers_smoker)
            #db.session.add(pers_name,pers_age,pers_sex,pers_bmi,pers_region,pers_children,pers_smoker)
            
            db.session.commit()
            return redirect("Results.html")
        
        except Exception as e:
            return f'There was an error adding details {e}'


        return render_template("Results.html")
    
    else:
        names2 = Friends.query.order_by(Friends.ID)
        return render_template("Results.html",input_data = inp_data, inputs = names2)
#"""

@app.route('/index')
def home():
    title='ML Tester'
    return render_template("text_form.html", title=title)