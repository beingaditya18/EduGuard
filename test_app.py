import streamlit as st
import google.generativeai as genai

st.write("Testing google-generativeai import")
try:
    genai.configure(api_key="AIzaSyDTQveZGXQ-MpTZxOGzp6Igb9zrHqSB83o") # Replace with your API key
    st.write("google-generativeai imported successfully!")
except ModuleNotFoundError:
    st.write("google-generativeai import failed.")
