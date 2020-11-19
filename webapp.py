import streamlit as st
from network_utils import *
from plot_utils import *
from graphs import FilterGraph,CycleGraph
from kbqa import get_answers,generate_answers
import pandas as pd

def display_network_analysis():
    st.header("Social Network Analysis")
    G = get_undirected_graph()
    options=['']
    for n in (list(G.nodes)):
        options.append(n)
    DG = get_directed_graph()
    S = FilterGraph(G)
    SDG = FilterGraph(DG)
    st.sidebar.header("Network Analysis")
    source = st.sidebar.selectbox(
            'Select Source Node',options )
    show_core = st.sidebar.checkbox('Display Core of the network')
    show_mvc = st.sidebar.checkbox('Display Most Important Members')
    show_cliques = st.sidebar.checkbox('Analyse Clusters/Cliques')
    show_msp = st.sidebar.checkbox('Analyse Min Span Tree')
    show_cycles = st.sidebar.checkbox('Show Cycles')
    dc = st.sidebar.checkbox('Degree Centrality')
    bc = st.sidebar.checkbox('Betweenness Centrality')
    cc = st.sidebar.checkbox('Closeness Centrality')
    ec = st.sidebar.checkbox('Eigen Centrality')

    if source!='':
        st.write("# Source Node View")
        filtered = S.filter_by_source(source)
        dg_filtered = SDG.filter_by_source(source)
        st.plotly_chart(plot3d(filtered,sourceNode=source))
        DG = dg_filtered
        G = filtered
    if show_core:
        st.write('# Are core actors effectively using their central position?')
        core_size = st.slider('Select Core Size', min_value=3, max_value=10, value=10,step=1)
        st.plotly_chart(plot3d(get_cores(DG,k=core_size)))
        
    if show_mvc:
        st.write('# Which websites to look at to get overall gist of the domain ?')
        st.pyplot(plot_cloud(get_vertex_cover(DG)))
        
    if show_cliques:
        st.write('# What spheres of influence do actors have within their network and beyond to drive the agenda?') 
        st.plotly_chart(plot3d(get_cliques(G)))

    if show_msp:
        st.write('# Network that allows information spread with least members') 
        st.plotly_chart(plot3d(get_min_span_tree(G)))    

    if show_cycles:
        st.write("# Analyse Cycles by cycle length")
        cycle_len = st.slider('Select Cycle Length', min_value=2, max_value=20, value=10,step=1)
        for cycle in get_simple_cycles(DG,cycle_len=cycle_len)[:10]:
            st.plotly_chart(plot_cycle(CycleGraph(cycle).graph()))
        
    if dc:
        st.write("# Who has the most connections in the network?")    
        st.pyplot(plot_cloud(get_degree_centrality(DG)))    
    if bc:
        st.write("# Who are the key intermediaries or bridges in the network?")
        st.pyplot(plot_cloud(get_betweeness_centrality(DG)))    
    if cc:
        st.write('# Who spreads information most easily across the network?')
        st.pyplot(plot_cloud(get_closeness_centrality(DG)))    
    if ec:
        st.write('# Who is most connected to central actors in the network?')
        st.pyplot(plot_cloud(get_eigen_centrality(DG)))    


def display_kbqa():
    st.header("Knowledge Base Question Answering")
    question = st.text_input("Please provide your query:",value=None)
    if question:
        if st.button('Evaluate'):
            data = get_answers(question)
            one_answer = generate_answers(question)
            #st.write(data)
            st.write("Retrieved knowledge:")
            st.table(pd.DataFrame(data,columns=["context","answer","meta"]))
            st.write("Specific answer:")
            st.table(one_answer)