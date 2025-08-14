import pickle
import streamlit as st
import pandas as pd
import numpy as np
import sklearn

with open("bp_prediction.pkl",'rb') as obj1:
    data=pickle.load(obj1)

st.title("Blood Pressure Prediction Model")
age=st.number_input('Enter you age:',0,100)
weight=st.number_input('Enter your weight in kg:',0,300)
height=st.number_input('Enter your height in cm:',1, 300)
exercise=st.number_input("Enter your exercise frequency:",0,30)

button=st.button('Predict')
if button:
    bmi=weight/(height/100)**2
    test=[[age,weight,height,bmi,exercise]]
    scaled=data['scaler'].transform(test)
    result=data['model'].predict(scaled)[0]
    st.success(f"Your predicted Systolic BP is {round(result,2)}mmHg")





