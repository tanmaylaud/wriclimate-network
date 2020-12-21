import streamlit as st
from .network_utils import *
from .plot_utils import *
from .graphs import FilterGraph,CycleGraph
import pandas as pd

def display_network_analysis():
    st.write("# Analysis of Website Network")
    st.write("Network analysis (NA) is a set of integrated techniques to depict relations among actors and to analyze the social structures that emerge from the recurrence of these relations. The basic assumption is that better explanations of social phenomena are yielded by analysis of the relations among entities.")
    st.write("<i> The size of nodes denotes their significance in the local network. The yellow nodes can be considered as most significant actors </i>",unsafe_allow_html=True)
    G = get_undirected_graph()
    options=['afr100.org']
    for n in (list(G.nodes)):
        options.append(n)
    DG = get_directed_graph()
    S = FilterGraph(G)
    SDG = FilterGraph(DG)
    st.sidebar.header("Network Analysis")
    show_source,dc,bc,cc,ec = False,False,False,False,False
    source = st.sidebar.selectbox(
            'Select Source Node',options)
    if source != '':
        show_source = st.sidebar.checkbox('Show Source Node View',value=True)
    selected_type = st.sidebar.radio(label='Analysis Type',options=['Display Core of the network','Display Most Important Members','Analyse Clusters/Cliques','Analyse Min Span Tree','Show Cycles','Analyse Centrality Measures'])
    
    if selected_type=='Analyse Centrality Measures':
        dc = st.sidebar.checkbox('Degree Centrality')
        bc = st.sidebar.checkbox('Betweenness Centrality')
        cc = st.sidebar.checkbox('Closeness Centrality')
        ec = st.sidebar.checkbox('Eigen Centrality')

    if show_source:
        st.write("<h3> <i> The size of nodes denotes their significance in the local network. The yellow nodes have higher importance in the local network of "+source+ "</i></h3>",unsafe_allow_html=True)
        st.write("# Source Node View")
        filtered = S.filter_by_source(source)
        dg_filtered = SDG.filter_by_source(source)
        st.plotly_chart(plot3d(filtered,sourceNode=source))
        DG = dg_filtered
        G = filtered
        if selected_type in ['Display Core of the network','Display Most Important Members','Analyse Clusters/Cliques','Analyse Min Span Tree','Show Cycles','Analyse Centrality Measures']:
            st.write("<h2><i> Analysis of Local Network of " + source + ": </i></h2>",unsafe_allow_html=True)
    if selected_type=='Display Core of the network':
        st.write('# Analysis of core actors in the network')
        st.write('### -based on the k-core decomposition algorithm.')
        st.write('<i>NOTE: If there is no graph, it means that the core size needs to be reduced, since not every local network is deep enough to have K layers. If at k=3 , a graph is not displayed, it indicates a shallow network </i>',unsafe_allow_html=True)
        core_size = st.slider('Select Core Size', min_value=3, max_value=10, value=5,step=1)
        fig = plot3d(get_cores(DG,k=core_size))
        if len(fig.data[0]['x'])!=0:
            st.plotly_chart(fig)
        else:
            st.write("#### No graph for core size:",core_size)
            st.write("#### Try reducing the core size for "+source+". Local network is probably shallow.")    

    if selected_type=='Display Most Important Members':
        st.write("#  Most Important Members (using Minimum Vertex Cover)")
        st.write('<h2><i> Which websites to look at to get overall gist of the domain ?</i></h2>',unsafe_allow_html=True)
        st.write('### -based on the vertex cover algorithm.')
        st.pyplot(plot_cloud(get_vertex_cover(DG)))

    if selected_type=='Analyse Clusters/Cliques':
        st.write("# Cliques/Clusters")
        st.write('<h2><i> What spheres of influence do actors have within their network and beyond to drive the agenda?</i></h2>',unsafe_allow_html=True)
        st.write('#### -based on the clique-finding algorithm.')
        st.write("<i> The size of nodes denotes their significance in the local network. The yellow nodes can be considered as cluster representatives </i>",unsafe_allow_html=True)
        st.plotly_chart(plot3d(get_cliques(G)))

    if selected_type=='Analyse Min Span Tree':
        st.write('<h1> Minimum Span Tree: </h1><h2><i>Network that allows information spread with least members</i></h2>',unsafe_allow_html=True)
        st.write('#### -based on the minimum span tree algorithm.')
        st.write('<i>NOTE: The algorithm will take considerable time when triggered without a source node. It will run fairly quickly when a source node is selected.</i>',unsafe_allow_html=True)
        st.plotly_chart(plot3d(get_min_span_tree(G)))

    if selected_type=='Show Cycles':
        st.write("# Analyse Cycles by cycle length")
        st.write('### -computed cycles in a directed graph')
        st.write('<i>NOTE: If there is no graph, it means that the cycle length needs to be reduced, since not every local network is deep enough to have K cycle length.</i>',unsafe_allow_html=True)
        cycle_len = st.slider('Select Cycle Length', min_value=2, max_value=20, value=10,step=1)
        cycle_exists = False
        i = 1
        for cycle in get_simple_cycles(DG,cycle_len=cycle_len)[:10]:
            cycle_exists=True
            st.write("### Cycle ",i)
            st.write("Scroll down for next cycle")
            st.plotly_chart(plot_cycle(CycleGraph(cycle).graph()))
            i +=1
        if not cycle_exists:
            st.write("#### No Cycle For Length:",cycle_len)
            st.write("#### Try reducing the cycle length. Local network is probably shallow")
    if dc:
        st.write("# Who has the most connections in the network?")
        st.write('### -based on the Degree Centrality algorithm.')
        st.write('### -Words with larger size have more connections in the local network')
        st.pyplot(plot_cloud(get_degree_centrality(DG)))
    if bc:
        st.write("# Who are the key intermediaries or bridges in the network?")
        st.write('### -based on the Betweenness Centrality algorithm.')
        st.write('### -Words with larger size are stronger bridges in the local network')
        st.pyplot(plot_cloud(get_betweeness_centrality(DG)))
    if cc:
        st.write('# Who spreads information most easily across the network?')
        st.write('### -based on the Closeness Centrality algorithm.')
        st.write('### -Words with larger size spread information better in the local network')
        st.pyplot(plot_cloud(get_closeness_centrality(DG)))
    if ec:
        st.write('# Who is most connected to central actors in the network?')
        st.write('### -based on the Eigen Centrality algorithm.')
        st.write('### -Words with larger size have more connections to central actors in the local network')
        st.pyplot(plot_cloud(get_eigen_centrality(DG)))
