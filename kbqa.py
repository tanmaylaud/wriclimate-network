import streamlit as st
import requests

@st.cache
def get_answers(question):
   json = {
       "query": question
   }
   return requests.post("http://ec2-100-27-49-93.compute-1.amazonaws.com:8000/search/pdfs",
                        json=json).json()["answers"]

@st.cache 
def generate_answers(question):
       json = {
       "query": question
       }
       resp = requests.post("http://ec2-100-27-49-93.compute-1.amazonaws.com:8000/generator/pdfs",
                        json=json).json()
       meta = resp["answers"][0]["meta"]["texts"]
       answers = resp["answers"][0]["answer"]
       return {"meta":meta, "answer":answers}