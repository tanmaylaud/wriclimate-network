import streamlit as st
from webapp import display_network_analysis, display_kbqa
st.header("WRI Dashboard Demo")
switch = st.sidebar.selectbox('Select Options',['Network Analysis','Knowledge Base QA'])

if switch == 'Network Analysis':
    display_network_analysis()
else:
    display_kbqa()