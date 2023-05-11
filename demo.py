
import streamlit as st
import pandas as pd
import altair as alt #graphics library

st.header("A simple demo of streamlit")

#st.info(f"We are using version{st.--version}")

st.write ("Hello from JGI!")
#st.sidebar.image("generic_logo.png")

st.sidebar.write("This is the side bar")

my_line = st.sidebar.radio("select things",
["Buying power","Dollar value","Inflation Rate"])