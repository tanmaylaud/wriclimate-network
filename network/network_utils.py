import networkx as nx
import pandas as pd
import streamlit as st
from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
from networkx.readwrite.pajek import read_pajek

@st.cache(allow_output_mutation=True)
def get_directed_graph():
    return nx.DiGraph(read_pajek("assets/DirectedGraph.paj"))

@st.cache(allow_output_mutation=True)
def get_undirected_graph():
    return nx.Graph(read_pajek("assets/UndirectedGraph.paj"))

def normalise(df):
    return pd.DataFrame(df-df.min())/(df.max()-df.min())

@st.cache
def get_degree_centrality(DG):
    dc = {k: v for k, v in sorted(nx.degree_centrality(DG).items(), key=lambda item: item[1],reverse=True)}
    dc = pd.DataFrame.from_dict(dc,orient='index')
    return normalise(dc)

@st.cache
def get_betweeness_centrality(DG):
    bc = {k: v for k, v in sorted(nx.betweenness_centrality(DG).items(), key=lambda item: item[1],reverse=True)}
    bc = pd.DataFrame.from_dict(bc,orient='index')
    return normalise(bc)

@st.cache
def get_closeness_centrality(DG):
    cc = {k: v for k, v in sorted(nx.closeness_centrality(DG).items(), key=lambda item: item[1],reverse=True)}
    cc = pd.DataFrame.from_dict(cc,orient='index')
    return normalise(cc)

@st.cache
def get_eigen_centrality(DG):
    ec = {k: v for k, v in sorted(nx.eigenvector_centrality(DG).items(), key=lambda item: item[1],reverse=True)}
    ec = pd.DataFrame.from_dict(ec,orient='index')
    return normalise(ec)

@st.cache(allow_output_mutation=True)
def get_simple_cycles(DG, cycle_len = 18 ):
    cycles = []
    for cycle in nx.simple_cycles(DG):
        if len(cycle)>cycle_len:
            cycles.append(cycle)
    return cycles

@st.cache(allow_output_mutation=True)
def get_cores(DG,k=None):
    Core = nx.k_core(DG,k=k)
    return Core

@st.cache(allow_output_mutation=True)
def get_min_span_tree(G):
    return nx.minimum_spanning_tree(G)

@st.cache(allow_output_mutation=True)
def get_vertex_cover(DG):
    mvc = min_weighted_vertex_cover(DG)
    return pd.DataFrame.from_dict({k: 1 for k in list(mvc)},orient='index')

@st.cache(allow_output_mutation=True)
def get_cliques(G):
    cliqs = nx.enumerate_all_cliques(G)
    CG = nx.Graph()
    for cliq in cliqs:
        if len(cliq)>3:
            for c in cliq:
                CG.add_node(c)
            for c1 in cliq:
                for c2 in cliq:
                    if c1!=c2:
                        CG.add_edge(c1,c2)
    return CG
