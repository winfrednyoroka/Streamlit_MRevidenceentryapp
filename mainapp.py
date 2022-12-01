import streamlit as st
import sqlite3 as sql

Mr_EvidenceDB =sql.connect("Mr_EvidenceDB")
c=Mr_EvidenceDB.cursor()
#create the tables if they do not exist
c.execute("""CREATE TABLE IF NOT EXISTS "effectsizetype" ("id" TEXT,"effectsizetype" TEXT,PRIMARY KEY("id"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "exposure" ("exposureid"	TEXT,"exposurename"	TEXT,PRIMARY KEY("exposureid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "methods" ("methodid" TEXT,"methodname" TEXT,PRIMARY KEY("methodid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "outcome" ("outcomeid" TEXT,"outcomename" TEXT,PRIMARY KEY("outcomeid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "study" ("pmid"	INTEGER,"title"	TEXT,"population" TEXT,"sex" TEXT,"mean_age" INTEGER,"median_age" INTEGER,"lower_age"INTEGER,"upper_age" INTEGER,"year" INTEGER,"samplesize" INTEGER,"author" TEXT,PRIMARY KEY("pmid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "results" ("results_id" TEXT,"pmid" INTEGER,"methodid" TEXT,"effectsize" REAL,"lowerinterval"	REAL,"upperinterval" REAL,"pvalue" REAL,"exposureid" TEXT,"outcomeid" TEXT,"effectsizetype_id" TEXT,PRIMARY KEY("results_id"));""")
def form():
    st.write("This is my data entry form")
    with st.form(key="STUDY", clear_on_submit=True):
        username=st.text_input("Enter your username")
        pmid=st.number_input("Enter the study pmid")
        title=st.text_input("Enter the study title")
        population=st.text_input("Enter the population/ancestry")
        sex=st.selectbox("sex of participants",["female","male","both"])
        mean_age=st.number_input("Enter the mean_age of the participants")
        median_age=st.number_input("Enter the median_age of the participants")
        lower_age=st.number_input("Enter the lower_age of the participants")
        upper_age=st.number_input("Enter the upper_age of the participants")
        year=st.number_input("Enter the year of pulication")
        samplesize=st.number_input("Enter the total sample size of the population under investigation")
        author=st.text_input("Enter the author names")
        submit_studybutton=st.form_submit_button(label="Submitstudyentry")
    with st.form(key="EXPOSURE",clear_on_submit=True):
        exposurename=st.text_input("Enter the name of the exposure under investigation")
        exposureid=st.number_input("Enter the unique identifer of exposure")
        submit_exposurebutton=st.form_submit_button(label="Submitexposureentry")
    with st.form(key="OUTCOME",clear_on_submit=True):
        outcomename=st.text_input("Enter the name of the outcome")
        outcomeid=st.number_input("Enter the unique outcome identifier")
        submit_outcomebutton=st.form_submit_button(label="Submitoutcomeentry")
    with st.form(key="METHOD",clear_on_submit=True):
        methodname=st.text_input("Enter the method name")
        methodid=st.number_input("Enter the unique ID of methods")
        submit_methodbutton=st.form_submit_button(label="Submitmethodentry")
    with st.form(key="EFFECTSIZE",clear_on_submit=True):
        id=st.number_input("Enter unique identifier for each of the effectsizetype")
        effectsizetype=st.text_input("Enter the effectsizetype")
        submit_effectsizebutton=st.form_submit_button(label="Submiteffectsizeentry")
    with st.form(key="RESULTS",clear_on_submit=True):
        resultsid=st.text_input("Enter the results id")
        effectsize=st.number_input("Enter the effcetsize")
        lowerinterval=st.number_input("Enter the lower CI")
        upperinterval=st.number_input("Enter the upper CI")
        pvalue=st.number_input("Enter the pvalue")
        #image=st.camera_input("Take a picture to upload")
        submit_button=st.form_submit_button(label="SUBMIT")
        if submit_button:
            adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue)
            
def adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue):
    """Populate the tables with data"""
    #c.execute("""CREATE TABLE IF NOT EXISTS "effectsizetype" ("id" TEXT,"effectsizetype" TEXT,PRIMARY KEY("id"));""")
    c.execute("INSERT INTO effectsizetype VALUES (?,?)",(id,effectsizetype))

    #c.execute("""CREATE TABLE IF NOT EXISTS "exposure" ("exposureid"	TEXT,"exposurename"	TEXT,PRIMARY KEY("exposureid"));""")
    c.execute("INSERT INTO exposure VALUES (?,?)",(exposureid,exposurename))

    #c.execute("""CREATE TABLE IF NOT EXISTS "methods" ("methodid" TEXT,"methodname" TEXT,PRIMARY KEY("methodid"));""")
    c.execute("INSERT INTO methods VALUES (?,?)",(methodid,methodname))

    #c.execute("""CREATE TABLE IF NOT EXISTS "outcome" ("outcomeid" TEXT,"outcomename" TEXT,PRIMARY KEY("outcomeid"));""")
    c.execute("INSERT INTO outcome VALUES (?,?)",(outcomeid,outcomename))

    #c.execute("""CREATE TABLE IF NOT EXISTS "study" ("pmid"	INTEGER,"title"	TEXT,"population" TEXT,"sex" TEXT,"mean_age" INTEGER,"median_age" INTEGER,"lower_age"INTEGER,"upper_age" INTEGER,"year" INTEGER,"samplesize" INTEGER,"author" TEXT,PRIMARY KEY("pmid"));""")
    c.execute("INSERT INTO study VALUES (?,?,?,?,?,?,?,?,?,?,?)",(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author))

    #c.execute("""CREATE TABLE IF NOT EXISTS "results" ("results_id" TEXT,"pmid" INTEGER,"methodid" TEXT,"effectsize" REAL,"lowerinterval"	REAL,"upperinterval" REAL,"pvalue" REAL,"exposureid" TEXT,"outcomeid" TEXT,"effectsizetype_id" TEXT,PRIMARY KEY("results_id"));""")
    c.execute("INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?)",(results_id,pmid,methodid,effectsize,lowerinterval,upperinterval,pvalue,exposureid,outcomeid,effectsizetype_id))
    Mr_EvidenceDB.commit()
    Mr_EvidenceDB.close()
    st.success("Hello {} you have entered the data for this study PMID {}".format(username,pmid))

form()