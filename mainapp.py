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
        st.subheader("STUDY TABLE")
        username=st.selectbox("Enter your username",["Winfred","Tom","Yi","Debbie","Chris"])
        pmid=st.number_input("Enter the study pmid",value=0)
        title=st.text_input("Enter the study title")
        population=st.selectbox("Enter the population/ancestry",["EUR","East Asian","Korean","AFR","AFR_AMR"])
        sex=st.selectbox("sex of participants",["female","male","both"])
        mean_age=st.number_input("Enter the mean_age of the participants")
        median_age=st.number_input("Enter the median_age of the participants")
        lower_age=st.number_input("Enter the lower_age of the participants")
        upper_age=st.number_input("Enter the upper_age of the participants")
        year=st.number_input("Enter the year of pulication",value=0)
        samplesize=st.number_input("Enter the total sample size of the population under investigation",value=0)
        author=st.text_input("Enter the author names")
        submit_studybutton=st.form_submit_button(label="Submitstudyentry")
        if submit_studybutton:
            adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,username)
    with st.form(key="EXPOSURE",clear_on_submit=True):
        st.subheader("EXPOSURE TABLE")
        st.write("E1:BMI,E2:Adiposity,E3:WHR,E4:childhoodBMI,E5:adultBMI,E6:fatmassindex,E7:fatfreemassindex,E8:FA,E9:UFA,E10:obesity,E11:bodyfat%,E12:BMIWGRS,E13:BMIGRS")
        exposurename=st.selectbox("exposure name",["BMI","Adiposity","WHR","childhoodBMI","adultBMI","fatmassindex","fatfreemassindex","FA","UFA","obesity","bodyfat%","BMIWGRS","BMIGRS"])
        exposureid=st.selectbox("Enter expid",["E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12","E13"])
        submit_exposurebutton=st.form_submit_button(label="Submitexposureentry")
        if submit_exposurebutton:
            expentry(exposurename,exposureid)
    with st.form(key="OUTCOME",clear_on_submit=True):
        st.subheader("OUTCOME TABLE")
        st.write("O1:incident hypertension,O2:ever hypertension,O3:hypertension,O4:gestational hypertension,O5:essential hypertension,O6:SBP,O7:DBP,O8:PAP,O9:PVremodelling,O10:Grade1diastolicdysfunction,O11:arterialhypertension")
        outcomename=st.selectbox("Enter the name of the outcome",["incident hypertension","ever hypertension","hypertension","gestational hypertension","essential hypertension","SBP","DBP","PAP","PVremodelling","Grade1diastolicdysfunction","arterial hypertension"])
        outcomeid=st.selectbox("Enter the unique outcome identifier",["O1","O2","O3","O4","O5","O6","O7","O8","O9","O10","O11"])
        submit_outcomebutton=st.form_submit_button(label="Submitoutcomeentry")
        if submit_outcomebutton:
            outentry(outcomename,outcomeid)
    with st.form(key="METHOD",clear_on_submit=True):
        st.subheader("METHOD TABLE")
        st.write("M1:IVW,M2:Wetmedian,M3:Wetmode,M4:MREgger,M5:IVestimator,M6:MVMR,M7:penalisedwetmedian,M8:SIMEXcorrectedMREgger,M9:MRGXE")
        methodname=st.selectbox("Enter the method name",["IVW","Wetmedian","Wetmode","MREgger","IVestimator","MVMR","penalisedwetmedian","SIMEXcorrectedMREgger","MRGXE"])
        methodid=st.selectbox("Enter the unique ID of methods",["M1","M2","M3","M4","M5","M6","M7","M8","M9"])
        submit_methodbutton=st.form_submit_button(label="Submitmethodentry")
        if submit_methodbutton:
            methodentry(methodname,methodid)
    with st.form(key="EFFECTSIZE",clear_on_submit=True):
        st.subheader("EFFECTSIZETYPE TABLE")
        st.write("ID1:OR,ID2:MD,ID3:HR,ID4:BETA")
        id=st.selectbox("Enter unique identifier for each of the effectsizetype",["ID1","ID2","ID3","ID4"])
        effectsizetype=st.selectbox("Enter the effectsizetype",["OR","MD","HR","BETA"])
        submit_effectsizebutton=st.form_submit_button(label="Submiteffectsizeentry")
        if submit_effectsizebutton:
            effectsizeentry(id,effectsizetype)
    with st.form(key="RESULTS",clear_on_submit=True):
        st.subheader("RESULTS TABLE")
        pmid=st.number_input("Enter the study pmid",value=0)
        st.write("M1:IVW,M2:Wetmedian,M3:Wetmode,M4:MREgger,M5:IVestimator,M6:MVMR,M7:penalisedwetmedian,M8:SIMEXcorrectedMREgger,M9:MRGXE")
        methodid=st.selectbox("Enter the unique ID of methods",["M1","M2","M3","M4","M5","M6","M7","M8","M9"])
        st.write("E1:BMI,E2:Adiposity,E3:WHR,E4:childhoodBMI,E5:adultBMI,E6:fatmassindex,E7:fatfreemassindex,E8:FA,E9:UFA,E10:obesity,E11:bodyfat%,E12:BMIWGRS,E13:BMIGRS")
        exposureid=st.selectbox("Enter expid",["E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12","E13"])
        st.write("O1:incident hypertension,O2:ever hypertension,O3:hypertension,O4:gestational hypertension,O5:essential hypertension,O6:SBP,O7:DBP,O8:PAP,O9:PVremodelling,O10:Grade1diastolicdysfunction,O11:arterial hypertension")
        outcomeid=st.selectbox("Enter the unique outcome identifier",["O1","O2","O3","O4","O5","O6","O7","O8","O9","O10","O11"])
        resultsid=st.text_input("Enter the results id")
        effectsize=st.number_input("Enter the effectsize",format="%.6f")
        st.write("ID1:OR,ID2:MD,ID3:HR,ID4:BETA")
        effectsizetype_id=st.selectbox("Enter unique identifier for each of the effectsizetype",["ID1","ID2","ID3","ID4"])
        lowerinterval=st.number_input("Enter the lower CI",format="%.6f")
        upperinterval=st.number_input("Enter the upper CI",format="%.6f")
        pvalue=st.number_input("Enter the pvalue",format="%.200f")
        se=st.number_input("Enter the standard error", format="%.6f")
        strata=st.text_input("Enter the stratification of results")
        #image=st.camera_input("Take a picture to upload")
        submit_button=st.form_submit_button(label="SUBMIT")
        if submit_button:
            resultsentry(resultsid,pmid,methodid,effectsize,lowerinterval,upperinterval,pvalue,exposureid,outcomeid,effectsizetype_id,se)
            #adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author)#exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue)
def expentry(a,b):
	c.execute("INSERT INTO exposure VALUES (?,?)",(a,b))
	Mr_EvidenceDB.commit()
    #Mr_EvidenceDB.close()

def outentry(a,b):
	c.execute("INSERT INTO outcome VALUES (?,?)",(a,b))
	Mr_EvidenceDB.commit()
    #Mr_EvidenceDB.close()
    
def resultsentry(a,b,d,e,f,g,h,i,j,k,l,m):
	c.execute("INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(a,b,d,e,f,g,h,i,j,k,l,m))
	Mr_EvidenceDB.commit()
    #st.success("HI! you have entered the Results for this results_id {}".format(resultsid))
    #Mr_EvidenceDB.close()

def methodentry(a,b):
	c.execute("INSERT INTO methods VALUES (?,?)",(a,b))
	Mr_EvidenceDB.commit()
    #Mr_EvidenceDB.close()

def effectsizeentry(a,b):
	c.execute("INSERT INTO effectsizetype VALUES (?,?)",(a,b))
	Mr_EvidenceDB.commit()
    #Mr_EvidenceDB.close()            
def adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,username):#,exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue):
    """Populate the tables with data"""
    #c.execute("""CREATE TABLE IF NOT EXISTS "effectsizetype" ("id" TEXT,"effectsizetype" TEXT,PRIMARY KEY("id"));""")
    #c.execute("INSERT INTO effectsizetype VALUES (?,?)",(id,effectsizetype))

    #c.execute("""CREATE TABLE IF NOT EXISTS "exposure" ("exposureid"	TEXT,"exposurename"	TEXT,PRIMARY KEY("exposureid"));""")
    #c.execute("INSERT INTO exposure VALUES (?,?)",(exposureid,exposurename))

    #c.execute("""CREATE TABLE IF NOT EXISTS "methods" ("methodid" TEXT,"methodname" TEXT,PRIMARY KEY("methodid"));""")
    #c.execute("INSERT INTO methods VALUES (?,?)",(methodid,methodname))

    #c.execute("""CREATE TABLE IF NOT EXISTS "outcome" ("outcomeid" TEXT,"outcomename" TEXT,PRIMARY KEY("outcomeid"));""")
    #c.execute("INSERT INTO outcome VALUES (?,?)",(outcomeid,outcomename))

    #c.execute("""CREATE TABLE IF NOT EXISTS "study" ("pmid"	INTEGER,"title"	TEXT,"population" TEXT,"sex" TEXT,"mean_age" INTEGER,"median_age" INTEGER,"lower_age"INTEGER,"upper_age" INTEGER,"year" INTEGER,"samplesize" INTEGER,"author" TEXT,PRIMARY KEY("pmid"));""")
    c.execute("INSERT INTO study VALUES (?,?,?,?,?,?,?,?,?,?,?)",(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author))

    #c.execute("""CREATE TABLE IF NOT EXISTS "results" ("results_id" TEXT,"pmid" INTEGER,"methodid" TEXT,"effectsize" REAL,"lowerinterval"	REAL,"upperinterval" REAL,"pvalue" REAL,"exposureid" TEXT,"outcomeid" TEXT,"effectsizetype_id" TEXT,PRIMARY KEY("results_id"));""")
    #c.execute("INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?)",(results_id,pmid,methodid,effectsize,lowerinterval,upperinterval,pvalue,exposureid,outcomeid,effectsizetype_id))
    Mr_EvidenceDB.commit()
    Mr_EvidenceDB.close()
    st.success("Hello {} you have entered the data for this study PMID {}".format(username,pmid))

form()