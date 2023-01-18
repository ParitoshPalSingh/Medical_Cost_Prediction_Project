# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:50:25 2023

@author: vmadmin
"""
import pandas as pd
import flask
from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

my_conn = create_engine("sqlite:///friends.db")

## Initialize the Database
db=SQLAlchemy(app)

## Create a DB model
class Friends(db.Model):
    ID = db.Column(db.Integer,primary_key=True,autoincrement=True)
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

@app.route('/delete/<int:id>')
def delete(id):
    delete_rec = Friends.query.get_or_404(id)
    
    try:
        db.session.delete(delete_rec)
        db.session.commit()
        return redirect("/Results") 
    except Exception as e:    
        return f'{e}'
    

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
            
            data1 = Friends(Name=name, Age=age, Sex=sex, Bmi=bmi, Region=region, Children=children,Smoker=smoker)
            
            db.session.add(data1)
            db.session.commit()
            
            id1=[];names1=[];age1=[];sex1=[];bmi1=[];Reg1=[];child1=[];smok1=[]
            names3 = Friends.query.order_by(Friends.ID)
            for i in names3:
                id1.append(i.ID)
                names1.append(i.Name)
                age1.append(i.Age)
                sex1.append(i.Sex)
                bmi1.append(i.Bmi)
                Reg1.append(i.Region)
                child1.append(i.Children)
                smok1.append(i.Smoker)
                
            
            df2 = pd.DataFrame({'ID':id1,'Name':names1,
                                'Age':age1,'Sex':sex1,'BMI':bmi1,'Region':Reg1,'Children':child1,'Smoker':smok1
                                })
            #df2 = pd.DataFrame(names_3)
            df2.to_csv('testing.csv')
            
            return redirect("/Results")
        
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


