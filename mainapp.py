import streamlit as st

import sqlite3

def form():
    st.write("This is my data entry form")
    with st.form(key="Data enytry", clear_on_submit=True):
        pmid=st.number_input("Enter the study pmid")
        title=st.text_input("Enter the study title")
        population=st.text_input("Enter the population/ancestry")
        sex=st.text_input("Enter the sex of the participants")
        mean_age=st.number_input("Enter the mean_age of the participants")
        median_age=st.number_input("Enter the median_age of the participants")
        lower_age=st.number_input("Enter the lower_age of the participants")
        upper_age=st.number_input("Enter the upper_age of the participants")
        year=st.number_input("Enter the year of pulication")
        samplesize=st.number_input("Enter the total sample size of the population under investigation")
        author=st.text_input("Enter the author names")
        exposurename=st.text_input("Enter the name of the exposure under investigation")
        exposureid=st.number_input("Enter the unique identifer of exposure")
        outcomename=st.text_input("Enter the name of the outcome")
        outcomeid=st.number_input("Enter the unique outcome identifier")
        methodname=st.text_input("Enter the method name")
        methodid=st.number_input("Enter the unique ID of methods")
        id=st.number_input("Enter unique identifier for each of the effectsizetype")
        effectsizetype=st.text_input("Enter the effectsizetype")
        effectsize=st.number_input("Enter the effcetsize")
        lowerinterval=st.number_input("Enter the lower CI")
        upperinterval=st.number_input("Enter the upper CI")
        pvalue=st.number_input("Enter the pvalue")

        


        #image=st.camera_input("Take a picture to upload")
        submit_button=st.form_submit_button(label="SUBMIT")

form()