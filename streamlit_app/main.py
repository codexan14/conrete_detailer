import streamlit as st
import requests

st.sidebar.title("Input Number")

x = st.number_input(label = "Input Number", min_value=0, max_value=100)
response = requests.get(f"http://127.0.0.1:8000", params={"number": x})
st.text(response.json()["number"])
