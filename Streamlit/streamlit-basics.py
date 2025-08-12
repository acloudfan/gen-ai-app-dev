# Streamlit basics - demo app

import streamlit as st

# Setup the title
st.title("demo streamlit app")

# Create a Selectbox in sidebar 
color = st.sidebar.selectbox(
    "Pick color",
    options = ('Red', 'Blue', 'White')
)

# Format the string & write it in main window
str = f"you picked : {color}"
st.write(str)

# Take user input as text
name = st.text_input(
    "Your name:",
    max_chars=50
)

# Format the string
str = f"your name is : {name}"

# Use Streamlit magic to write the string to main window
str

