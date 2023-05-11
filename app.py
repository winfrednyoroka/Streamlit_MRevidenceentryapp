#load the libraries
import streamlit as st
import pandas as pd
#sidebar
st.sidebar.header("This is the sidebar")
def main():
    st.title("Data entry form")
    st.subheader("Follow through the forms to populate the database")
    st.help(st.form)
    menu = ["Home","About"]
    choice=st.sidebar.selectbox("Menu",menu)
    
    if choice=="Home":
        st.subheader("Dataentry forms")
    #salary calculator
        with st.form(key='salarycalculator',clear_on_submit=True):
            col1,col2,col3= st.columns([3,2,1])

            with col1:
                amount=st.number_input('Hourly Rate in $')
            with col2:
                hour_per_week = st.number_input('Hours per week',1,120)
            with col3:
                st.text("salary")
                submit_salary=st.form_submit_button(label='calculate')
        if submit_salary:   
            with st.expander("Results"):
                daily=[amount *8]
                weekly=[amount*hour_per_week]
                df=pd.DataFrame({'hourly':amount,"daily":daily,"weekly":"weekly"})
                st.dataframe(df.T)


        #context approach
        with st.form (key='form1',clear_on_submit=True):
            fname= st.text_input("fname")
            lname=st.text_input('lname')
            dob=st.date_input("date of birth")
            submit_button=st.form_submit_button(label="Submit")

            #the ooutput of my data entry can be within or without the file
        if submit_button:
            st.success("Hello {} you have successuflly entered your data".format(fname))
#alternative method for data entry
        form2 =st.form(key='form2')
        username=form2.text_input("username")
        jobtype=form2.selectbox("job",["Dev","Data scientist","Doctor"])
        submit_button1=form2.form_submit_button("login")
        if submit_button1:
            st.success("Hello {}.{} you have successfully entered your details".format(jobtype,username))


    else:
        st.subheader("About")
        st.write("You have to slect home in menu section for you to enter the data")



if  __name__=='__main__':
    main()