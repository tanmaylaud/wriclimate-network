from .plot_utils import get_graph_fig
from .plot_utils3d import get_graph_fig3D
from .graphs import FilterKGraph,get_graph,get_ner_list,get_ner_definition,get_relation_table
import streamlit as st

def display_knowledge_graph():
    st.write("# Knowledge Graphs ")
    st.write("### Select source node in sidebar to determine relationships")
    G = get_graph()
    nodes =['ABC']
    for n in G.nodes:
        if G.nodes[n]["node_type"]=="subject":
            nodes.append(n)
    display_graph = get_graph_fig        
    node = st.sidebar.selectbox('Source Node', options=nodes)
    view = st.sidebar.radio(label= 'Select View', options=['2D','3D'])
    if view =='3D':
        display_graph = get_graph_fig3D
    ners = st.sidebar.multiselect('Entity Type',options=get_ner_list(),default='ALL')
    if node != '':
        FG = FilterKGraph(G).filter_by_source(node)
        if 'ALL' in ners or len(ners)==0:
            st.plotly_chart(display_graph(FG.graph()))
            st.write(get_relation_table(FG.graph()),unsafe_allow_html=True)
        else:
            S = FG.filter_by_ner(ners)
            st.plotly_chart(display_graph(S.graph()))
            st.write(get_relation_table(S.graph()),unsafe_allow_html=True)
    st.write("### Reference Table for entity selection:")
    st.write(get_ner_definition(),unsafe_allow_html=True)    