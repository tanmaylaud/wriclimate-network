import streamlit as st
from network_utils import *
from plot_utils import *
from graphs import FilterGraph

st.header("Social Network Analysis")
G = get_undirected_graph()
options=['']
for n in (list(G.nodes)):
    options.append(n)
DG = get_directed_graph()
S = FilterGraph(G)
st.sidebar.header("Options")
source = st.sidebar.selectbox(
        'Select Source Node',options )
show_core = st.sidebar.checkbox('Display Core of the network')
show_mvc = st.sidebar.checkbox('Display Most Important Members')
show_cliques = st.sidebar.checkbox('Analyse Clusters/Cliques')

if source!='':
    st.write("# Source Node View")
    filtered = S.filter_by_source(source)
    st.pyplot(plot(filtered))
    
if show_core:
    st.write('# Are core actors effectively using their central position?')
    st.pyplot(plot(get_cores(DG)))
    
if show_mvc:
    st.write('# Which websites to look at to get overall gist of the domain ?')
    st.pyplot(plot_cloud(get_vertex_cover(DG)))
    
if show_cliques:
    st.write('# What spheres of influence do actors have within their network and beyond to drive the agenda?') 
    st.pyplot(plot(get_cliques(G)))
    
st.write("# Who has the most connections in the network?")    
st.pyplot(plot_cloud(get_degree_centrality(DG)))    
st.write("# Who are the key intermediaries or bridges in the network?")
st.pyplot(plot_cloud(get_betweeness_centrality(DG)))    
st.write('# Who spreads information most easily across the network?')
st.pyplot(plot_cloud(get_closeness_centrality(DG)))    
st.write('# Who is most connected to central actors in the network?')
st.pyplot(plot_cloud(get_eigen_centrality(DG)))    

