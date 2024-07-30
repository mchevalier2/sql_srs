import streamlit as st
import pandas as pd
import duckdb

st.write('''
    # SQL SRS
    Spaced Repetition System SQL Practice
    ''')

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Select contact method+"
)

st.write("You select:", option)

data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
with tab1:
    sql_query = st.text_area("label text")
    st.write(f"Vous avez rentré la requete: {sql_query}")
    result = duckdb.query(sql_query).df()
    st.dataframe(result)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples.dog.jpg", width=200)

with tab3:
    st.header("an aowl")
