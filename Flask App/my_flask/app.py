# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:50:25 2023

@author: vmadmin
"""
import pandas as pd
import numpy as np
import flask
from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


my_conn = create_engine("sqlite:///users.db")

## Initialize the Database
db2=SQLAlchemy(app)

## Create a DB model
class Users(db2.Model):
    ID = db2.Column(db2.Integer,primary_key=True,autoincrement=True)
    Name = db2.Column(db2.String(50),primary_key=False,nullable=False)
    Age = db2.Column(db2.Integer,nullable=False)
    Sex = db2.Column(db2.String(6),nullable=False)
    Bmi = db2.Column(db2.Float,nullable=False)
    Region = db2.Column(db2.String(12),nullable=False)
    Children = db2.Column(db2.Integer,nullable=False)
    Smoker = db2.Column(db2.String(4),nullable=False)
    Insurance = db2.Column(db2.Integer,nullable=False)
    
#    def __init__(self, thewords):
#        self.words = thewords
        
    #Function that will return a string 
    #def __repr__(self):
    #    return '<Names %r' % self.ID


with app.app_context():
    db2.create_all()
    


inp_data=[]

@app.route('/delete/<int:id>')
def delete(id):
    print('trigger1')
    delete_rec2 = Users.query.get_or_404(id)
    print('Delete triggered')
    
    try:
        db2.session.delete(delete_rec2)
        db2.session.commit()
        print('test22222')
        
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

import pickle
#Loading saved Model
pickled_rf_reg = pickle.load(open('pickles/rf_reg.pkl','rb'))
print(pickled_rf_reg)
cnt_id = 0

@app.route('/Results',methods=['POST','GET'])
def Results():
    if request.method=="POST":
        id1=[];names1=[];age1=[];sex1=[];bmi1=[];Reg1=[];child1=[];smok1=[]
        cnt_id=+1;
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        bmi = request.form.get('bmi')
        region = request.form.get('region')
        children = request.form.get('children')
        smoker = request.form.get('smoker')
        
        #### Getting the Prediction for each entry ####
        id1.append(cnt_id);names1.append(name);age1.append(int(age));sex1.append(sex);bmi1.append(float(bmi));
        Reg1.append(region);child1.append(int(children));smok1.append(smoker)
        
        df_testing = pd.DataFrame({'ID':id1,'Name':names1,'Age':age1,'Sex':sex1,'BMI':bmi1,'Region':Reg1,'Children':child1,'Smoker':smok1})
        
        df_custom = df_testing[['Name','Age','BMI','Children','Sex','Smoker','Region']]
        dfnew = df_custom.rename({'Name':'name','Age':'age','Sex':'sex','BMI':'bmi','Region':'region','Children':'children','Smoker':'smoker'},axis=1).copy()
        
        dfnew['sex'] = dfnew['sex'].replace(['M','F'],['male','female'])
        dfnew['smoker'] = dfnew['smoker'].replace({'No':'no','Yes':'yes'})
        
        dfnew.drop('name',axis=1,inplace=True)
        df_dummies = dfnew.copy()

        ## The problem is that when I only take one value then I can't dynamically decide on all different values i.e., classes
        ## this when resolved will allow for the pickle file to run
        
        #age,bmi,children,sex__female,sex__male,smoker__no,smoker__yes,region__northeast,region__northwest,region__southeast,region__southwest
        
        #for i in df_dummies.columns:
            #if df_dummies[i].dtype=='object':
                #dummies = pd.get_dummies(df_dummies[i], prefix=f'{i}_')
                #df_dummies = pd.concat([df_dummies, dummies], axis=1)
                #df_dummies = df_dummies.drop(i,axis=1)
        
        
        dfnew1 = dfnew.copy()
        
        #dfnew1[dfnew1['sex'] == 'male']
        dfnew1['sex__female'] = np.where(dfnew1.sex == 'female', '1', '0')
        dfnew1['sex__male'] = np.where(dfnew1.sex == 'male', '1', '0')
        
        dfnew1['smoker__no'] = np.where(dfnew1.smoker == 'no', '1', '0')
        dfnew1['smoker__yes'] = np.where(dfnew1.smoker == 'yes', '1', '0')
        
        
        dfnew1['region__northeast'] = np.where(dfnew1.region == 'northeast', '1', '0')
        dfnew1['region__northwest'] = np.where(dfnew1.region == 'northwest', '1', '0')
        dfnew1['region__southeast'] = np.where(dfnew1.region == 'southeast', '1', '0')
        dfnew1['region__southwest'] = np.where(dfnew1.region == 'southwest', '1', '0')
        
        dfnew1.drop(['sex','smoker','region'],axis=1,inplace=True)
        
        preds = int(pickled_rf_reg.predict(dfnew1)[0])

        
        ###############################################
        
        pers_age=Users(Age=age);
        pers_name = Users(Name=name);
        pers_sex = Users(Sex=sex);pers_bmi=Users(Bmi=bmi);
        pers_region = Users(Region=region);pers_children=Users(Children=children);
        pers_smoker = Users(Smoker = smoker)
        pers_ins = Users(Insurance=preds)
        #return render_template("Results.html", friends=newtestdata)
        inp_data.append(f"{name}|{age}|{sex}|{bmi}|{region}|{children}|{smoker}|{preds}")
        #return render_template("Results.html",input_data = inp_data)
        
        try:
            
            data111 = Users(Name=name, Age=age, Sex=sex, Bmi=bmi, Region=region, Children=children,Smoker=smoker, Insurance=preds)
            
            db2.session.add(data111)
            db2.session.commit()
            
            return redirect("/Results")
        
        except Exception as e:
            return f'There was an error adding details {e}'


        return render_template("Results.html")
    
    else:
        names2 = Users.query.order_by(Users.ID)
        return render_template("Results.html",input_data = inp_data, inputs = names2)
#"""

@app.route('/index')
def home():
    title='ML Tester'
    return render_template("text_form.html", title=title)

@app.route('/g.gif')
def g():
    return render_template("g.gif")

@app.route('/l.gif')
def l():
    return render_template("l.gif")



@app.route('/styling.css')
def home2():
    title='ML Tester'
    return render_template("text_form.html", title=title)

