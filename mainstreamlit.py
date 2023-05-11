import streamlit as st
import pandas as pd
import sqlite3 

header =st.container()
dataset =st.container()


with header:
    st.title("Welcome to my data entry form")
    st.text("This form allows me to enter data once I extract from papers")


with dataset:
    st.header("some dataset")

def main():
    st.title("database dataentryform")
    menu=["Home","About"]
    choice=st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Homepage")

    else:
        st.subheader("About")


if __name__=='__main__':
    main()

    