'''
Streamlit testing script to test deployment on Heroku
'''

import streamlit as st
import os
st.title('Streamlit Turoial App')
st.write('Testing for deployment')

st.write('Testing using Heroku DATABASE_URL envi var')
db_url = os.environ['DATABASE_URL']
st.write(db_url[-10:])


button1 = st.button("Click Me")
if button1:
    st.write("This is some text.")

st.header("Checkbox Section")
like = st.checkbox("Do you like this app?")
button2 = st.button("Submit")
if button2:
    if like:
        st.write("Thanks. I like it too.")
    else:
        st.write("I am sad.")

st.header("Start of the Radio Button Section")
animal = st.radio("What animal is your favorite?",
("Lion","Tiger","Bull")
)
button3 = st.button("Submit Animal")
if button3:
    st.write(animal)
    if animal == "Lion":
        st.write("ROAR!")

st.header("Start of the SelectBox Button Section")
animal2 = st.selectbox("What animal is your favorite?",
("Lion","Tiger","Bull")
)
button4 = st.button("Submit Animal2")
if button4:
    st.write(animal2)
    if animal2 == "Lion":
        st.write("ROAR!")

st.header("Start of the MultiSelectBox Button Section")
animal3 = st.multiselect("What animal is your favorite?",
("Lion","Tiger","Bull")
)
button5 = st.button("Submit Animal3")
if button5:
    st.write(animal3)

st.header("Start of the Slider Section")
epochs_num = st.slider("How many epochs?", 1, 100,10) # min,max, default

st.header("Start of the Text Input Section")
user_text = st.text_input("what is your favourite movie?", "Interstellar")
if st.button("text Button"): # need not to define button as a variable!
    st.write(user_text) # Optional to cast type as int, or as follow
user_num = st.number_input("what is your favourite number?")
if st.button("num Button"):
    st.write(user_num)

txt = st.text_area('','Just do it.') # Title, text in the text box
st.write(txt)