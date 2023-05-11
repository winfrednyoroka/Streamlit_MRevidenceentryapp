import streamlit as st
import sqlite3 as sql
#Use a different name to avoid overwriting the previous database in mainapp.py
#The new database has additional table known as studynotes
Mr_EvidenceDB_30_03_2023 =sql.connect("Mr_EvidenceDB_30_03_2023")
c=Mr_EvidenceDB_30_03_2023.cursor()
#create the tables if they do not exist
c.execute("""CREATE TABLE IF NOT EXISTS "effectsizetype" ("id" TEXT,"effectsizetype" TEXT,PRIMARY KEY("id"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "exposure" ("Exposureid_resultsid" TEXT,"exposureid" TEXT, "exposurename" TEXT,"exposuremeasured" TEXT,"resultsid" TEXT,"exposurenotes" TEXT,PRIMARY KEY("Exposureid_resultsid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "methods" ("methodid" TEXT,"methodname" TEXT,PRIMARY KEY("methodid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "outcome" ("outcomeid_resultsid" TEXT,"outcomeid" TEXT,"outcomename" TEXT,"outcomemeasured" TEXT,"resultsid" TEXT,"totalsamplesize_outcome" INTEGER," cases_outcome" INTEGER,"control_outcome" INTEGER,"outcomenotes" TEXT,PRIMARY KEY("outcomeid_resultsid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "study" ("pmid"	INTEGER,"title"	TEXT,"studyaim" TEXT,"population" TEXT,"sex" TEXT,"mean_age" INTEGER,"median_age" INTEGER,"lower_age"INTEGER,"upper_age" INTEGER,"year" INTEGER,"samplesize" INTEGER,"author" TEXT,PRIMARY KEY("pmid"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "results" ("results_id" TEXT,"pmid" INTEGER,"methodid" TEXT,"effectsize" REAL,"lowerinterval"	REAL,"upperinterval" REAL,"pvalue" REAL, "se" REAL,"exposureid" TEXT,"outcomeid" TEXT,"effectsizetype_id" TEXT, "strata" TEXT,PRIMARY KEY("results_id"));""")
c.execute("""CREATE TABLE IF NOT EXISTS "studynotes" ("notesid" TEXT,"pmid" INTEGER,"resultsid" TEXT,"no_ofIVs" INTEGER,"analysistype" TEXT, "unitsofmeasurement" TEXT,"notes" TEXT, PRIMARY KEY("notesid"));""")
def form():
    st.write("This is my data entry form")
    with st.form(key="STUDY", clear_on_submit=True):
        st.subheader("STUDY TABLE")
        username=st.selectbox("Enter your username",["Winfred","Tom","Yi","Debbie","Chris","Maria"])
        pmid=st.number_input("Enter the study pmid",value=0)
        title=st.text_input("Enter the study title")
        studyaim=st.text_input("Enter the aim of the study")
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
            adddata(pmid,title,studyaim,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,username)
    with st.form(key="EXPOSURE",clear_on_submit=True):
        st.subheader("EXPOSURE TABLE")
        st.write("E1_BMI E2_WHR E3_GRS E4_weightedGRS E5_WHtR")
        exposureid_resultsid=st.text_input("Enter the exposureid and resultsid separated by underscore")
        exposureid=st.selectbox("Enter expid",["E1","E2","E3","E4","E5"])
        exposurename=st.selectbox("exposure name",["BMI","WHR","GRS","weightedGRS","WHtR"])
        exposuremeasured=st.text_input("Enter details of how the exposure was measured")
        resultsid=st.text_input("Enter the results identifier")
        #totalsamplesize_exposure=st.number_input("Enter the total sample size associated with exposure")
        #cases_exposure=st.number_input("Enter the number of cases associated with exposure")
        #control_exposure=st.number_input("Enter the number of controls associated with exposure")
        exposurenotes=st.text_input("Enter details of the exposure for instance adult or childhood or weight scores")
        submit_exposurebutton=st.form_submit_button(label="Submitexposureentry")
        if submit_exposurebutton:
            expentry(exposureid_resultsid,exposureid,exposurename,exposuremeasured,resultsid,exposurenotes)
    with st.form(key="OUTCOME",clear_on_submit=True):
        st.subheader("OUTCOME TABLE")
        st.write("O1_hypertension O2_SBP O3_DBP O4_PAP O5_PVremodelling O6_Grade1diastolicdysfunction")
        outcomeid_resultsid=st.text_input("Enter the outcomeid and resultsid separated by underscore")
        outcomeid=st.selectbox("Enter the unique outcome identifier",["O1","O2","O3","O4","O5","O6"])
        outcomename=st.selectbox("Enter the name of the outcome",["hypertension","SBP","DBP","PAP","PVremodelling","Grade1diastolicdysfunction"])
        outcomemeasured=st.text_input("Enter details of how the outcome was measured")
        resultsid=st.text_input("Enter the results identifier")
        totalsamplesize_outcome=st.number_input("Enter the total sample size associated with outcome")
        cases_outcome=st.number_input("Enter the number of cases associated with outcome")
        control_outcome=st.number_input("Enter the number of controls associated with outcome")
        outcomenotes=st.text_input("Enter details of the outcome for instance gestational or ever or incident hypertension")
        submit_outcomebutton=st.form_submit_button(label="Submitoutcomeentry")
        if submit_outcomebutton:
            outentry(outcomeid_resultsid,outcomeid,outcomename,outcomemeasured,resultsid,totalsamplesize_outcome,cases_outcome,control_outcome,outcomenotes)
    with st.form(key="METHOD",clear_on_submit=True):
        st.subheader("METHOD TABLE")
        st.write("M1_IVW M2_Wetmedian M3_Wetmode M4_MREgger M5_IVestimator M6_MVMR M7_penalisedwetmedian M8_SIMEXcorrectedMREgger M9_MRGXE,M10_TSLS M11_MR-PRESSO M12_Contaminationmixture M13_MR-LDP M14_RAPS M15_LDA_MRE MR16_LDMR M17_PLDMRa M18_PLDMR")
        methodname=st.selectbox("Enter the method name",["IVW","Wetmedian","Wetmode","MREgger","IVestimator","MVMR","penalisedwetmedian","SIMEXcorrectedMREgger","MRGXE","TSLS","MR-PRESSO","Contaminationmixture"])
        methodid=st.selectbox("Enter the unique ID of methods",["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18"])
        submit_methodbutton=st.form_submit_button(label="Submitmethodentry")
        if submit_methodbutton:
            methodentry(methodname,methodid)
    with st.form(key="EFFECTSIZE",clear_on_submit=True):
        st.subheader("EFFECTSIZETYPE TABLE")
        st.write("ID1_OR ID2_MD ID3_HR ID4_BETA ID5_RiskDifference")
        id=st.selectbox("Enter unique identifier for each of the effectsizetype",["ID1","ID2","ID3","ID4","ID5"])
        effectsizetype=st.selectbox("Enter the effectsizetype",["OR","MD","HR","BETA","RiskDifference"])
        submit_effectsizebutton=st.form_submit_button(label="Submiteffectsizeentry")
        if submit_effectsizebutton:
            effectsizeentry(id,effectsizetype)
    with st.form(key="RESULTS",clear_on_submit=True):
        st.subheader("RESULTS TABLE")
        pmid=st.number_input("Enter the study pmid",value=0)
        st.write("M1_IVW M2_Wetmedian M3_Wetmode M4_MREgger M5_IVestimator M6_MVMR M7_penalisedwetmedian M8_SIMEXcorrectedMREgger M9_MRGXE,M10_TSLS M11_MR-PRESSO M12_Contaminationmixture M13_MR-LDP M14_RAPS M15_LDA_MRE MR16_LDMR M17_PLDMRa M18_PLDMR")
        methodid=st.selectbox("Enter the unique ID of methods",["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18"])
        st.write("E1_BMI E2_WHR E3_GRS E4_weightedGRS E5_WHtR")
        exposureid=st.selectbox("Enter expid",["E1","E2","E3","E4","E5"])
        st.write("O1_hypertension O2_SBP O3_DBP O4_PAP O5_PVremodelling O6_Grade1diastolicdysfunction")
        outcomeid=st.selectbox("Enter the unique outcome identifier",["O1","O2","O3","O4","O5","O6"])
        resultsid=st.text_input("Enter the results id")
        effectsize=st.number_input("Enter the effectsize",format="%.6f")
        #st.write("Here's our first attempt at using data to create a table:")
        st.write("ID1_OR ID2_MD ID3_HR ID4_BETA ID5_RiskDifference")
        effectsizetype_id=st.selectbox("Enter unique identifier for each of the effectsizetype",["ID1","ID2","ID3","ID4","ID5"])
        lowerinterval=st.number_input("Enter the lower CI",format="%.6f")
        upperinterval=st.number_input("Enter the upper CI",format="%.6f")
        pvalue=st.number_input("Enter the pvalue",format="%.200f")
        se=st.number_input("Enter the standard error", format="%.6f")
        strata=st.text_input("Enter the stratification of results")
        #image=st.camera_input("Take a picture to upload")
        submit_button=st.form_submit_button(label="SUBMIT")
        if submit_button:
            resultsentry(resultsid,pmid,methodid,effectsize,lowerinterval,upperinterval,pvalue,exposureid,outcomeid,effectsizetype_id,se,strata)
            #adddata(pmid,title,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author)#exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue)
    with st.form(key="STUDYNOTES", clear_on_submit=True):
        st.subheader("STUDYNOTES TABLE")
        notesid=st.text_input("Enter the note identifier starting from N1")
        pmid=st.number_input("Enter the study pmid",value=0)
        resultsid =st.text_input("Enter the resultsid")
        #st.write("M1_IVW M2_Wetmedian M3_Wetmode M4_MREgger M5_IVestimator M6_MVMR M7_penalisedwetmedian M8_SIMEXcorrectedMREgger M9_MRGXE,M10_TSLS M11_MR-PRESSO M12_Contaminationmixture M13_MR-LDP M14_RAPS M15_LDA_MRE MR16_LDMR M17_PLDMRa M18_PLDMR")
        #methodid=st.selectbox("Enter the unique ID of methods",["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18"])
        no_ofIVs=st.number_input("Enter the number of instrumnets in GRS",value=0)
        analysistype=st.selectbox("Enter the type of analysis either main or secondary/sensitivity",["Main","secondary","sensitivity"])  
        unitsofmeasurement=st.text_input("Enter the units of measurement reported by the paper")
        notes=st.text_input("Enter additional information that may seem relevant to analysis")
        submit_studynotesbutton=st.form_submit_button(label="submitstudynotes")
        if submit_studynotesbutton:
            studynotesentry(notesid,pmid,no_ofIVs,analysistype,resultsid,unitsofmeasurement,notes)

def studynotesentry(a,b,d,e,f,g,h):
    c.execute("INSERT INTO studynotes VALUES (?,?,?,?,?,?,?)",(a,b,d,e,f,g,h))
    Mr_EvidenceDB_30_03_2023.commit()
def expentry(a,b,d,e,f,g):
	c.execute("INSERT INTO exposure VALUES (?,?,?,?,?,?)",(a,b,d,e,f,g))
	Mr_EvidenceDB_30_03_2023.commit()
    #Mr_EvidenceDB.close()

def outentry(a,b,d,e,f,g,h,i,j):
	c.execute("INSERT INTO outcome VALUES (?,?,?,?,?,?,?,?,?)",(a,b,d,e,f,g,h,i,j))
	Mr_EvidenceDB_30_03_2023.commit()
    #Mr_EvidenceDB.close()
    
def resultsentry(a,b,d,e,f,g,h,i,j,k,l,m):
	c.execute("INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(a,b,d,e,f,g,h,i,j,k,l,m))
	Mr_EvidenceDB_30_03_2023.commit()
    #st.success("HI! you have entered the Results for this results_id {}".format(resultsid))
    #Mr_EvidenceDB.close()

def methodentry(a,b):
	c.execute("INSERT INTO methods VALUES (?,?)",(a,b))
	Mr_EvidenceDB_30_03_2023.commit()
    #Mr_EvidenceDB.close()

def effectsizeentry(a,b):
	c.execute("INSERT INTO effectsizetype VALUES (?,?)",(a,b))
	Mr_EvidenceDB_30_03_2023.commit()
    #Mr_EvidenceDB.close()            
def adddata(pmid,title,studyaim,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author,username):#,exposurename,exposureid,outcomename,outcomeid,methodname,methodid,id,effectsizetype,resultsid,effectsize,lowerinterval,upperinterval,pvalue):
    """Populate the study table with data"""
    c.execute("INSERT INTO study VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(pmid,title,studyaim,population,sex,mean_age,median_age,lower_age,upper_age,year,samplesize,author))

    Mr_EvidenceDB_30_03_2023.commit()
    Mr_EvidenceDB_30_03_2023.close()
    st.success("Hello {} you have entered the data for this study PMID {}".format(username,pmid))

form()