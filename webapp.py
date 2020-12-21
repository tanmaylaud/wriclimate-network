import pandas as pd
import numpy as np
import json

import streamlit as st
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px

from network.webapp import display_network_analysis
from knowledge_graph.webapp import display_knowledge_graph


st.set_page_config(
	layout="wide"
)

st.sidebar.markdown('# WRI Climate Adaptation Interface')
st.sidebar.markdown('# Navigation')

st.sidebar.write('### Select analysis category')
analysis = st.sidebar.radio('Select one of the following: ', ['Network Analysis' , 'Knowledge Graphs'], index=0)
if analysis == 'Network Analysis':
    display_network_analysis()
elif analysis == 'Knowledge Graphs':
    display_knowledge_graph()
