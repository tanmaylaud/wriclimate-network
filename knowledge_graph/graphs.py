import networkx as nx
from networkx.readwrite import read_yaml
import streamlit as st
import pickle
import pandas as pd

class FilterKGraph():
  def __init__(self,G, sourceNode=None, relevant_nodes = None):
    self.G = G
    self.sourceNode = sourceNode
    self.relevant_nodes = relevant_nodes
    
  def _filter_node(self,x):
    if self.sourceNode == x:
      return True
    if x in self.nodes:
      return True
    return False

  def _filter_ner(self,x):
    if x in self.relevant_nodes:
      return True  
    if x in self.G.nodes:
      for ner in self.ners:
        if ner in self.G.nodes[x]["ner"]:
          return True
    return False    

  def get_closest_nodes_to_query(self,q):
    self.relevant_nodes = []
    for n in self.G.nodes:
      if q in n and self.G.nodes[n]["node_type"]=="subject":
        self.relevant_nodes.append(n)
    return self.relevant_nodes

  def updateNodes(self,x):
    relevant_nodes = self.get_closest_nodes_to_query(x)
    self.nodes = set()
    for node in relevant_nodes:
      self.nodes.add(node)
      for desc in nx.algorithms.traversal.breadth_first_search.descendants_at_distance(self.G,node,1):
        self.nodes.add(desc)

  def filter_by_ner(self,ners):
    self.ners = ners
    return FilterKGraph(nx.subgraph_view(self.G,filter_node=self._filter_ner),self.sourceNode,self.relevant_nodes)   

  def filter_by_source(self,sourceNode):
    self.sourceNode = sourceNode
    self.updateNodes(sourceNode)
    return FilterKGraph(nx.subgraph_view(self.G,filter_node=self._filter_node),self.sourceNode,self.relevant_nodes)  
  
  def graph(self):
    return self.G

@st.cache(allow_output_mutation=True)
def get_graph():
    return nx.DiGraph(pickle.load(open("assets/KnowledgeGraph.pkl",'rb')))

def get_ner_list():
    return ['ALL','CARDINAL','DATE','EVENT','FAC','GPE','LANGUAGE','LAW',
             'LOC','MONEY','NORP','ORDINAL','ORG','PERCENT','PERSON',
             'PRODUCT','QUANTITY','TIME','WORK_OF_ART']

@st.cache(allow_output_mutation=True)     
def get_ner_definition():
    df = pd.DataFrame.from_dict(
      {"PERSON" : "People, including fictional characters.",
        "NORP" : "Nationalities, Religions or Political groups.",
        "FAC" : "Facilities like buildings, bridges, etc.",
        "ORG" : "Organizations, Companies, Institutions, etc.",
        "GPE" : "Geo-political entities like countries, states etc.",
        "LOC" : "Locations like mountains, bodies of water etc.",
        "PRODUCT" : "Objects, vehicles, foods, etc. (Not services)",
        "EVENT" : "Named events like hurricanes, battles, wars, etc.",
        "WORK_OF_ART" : "Titles of books, songs, etc.",
        "LAW" : "Law-related Documents.",
        "LANGUAGE" : "Any named language.",
        "DATE" : "Dates or periods.",
        "TIME"	: "Times smaller than a day.",
        "PERCENT" : "Percentage, including '%'.",
        "MONEY" : "Monetary values, including unit.",
        "QUANTITY" : "Measurements like weight or distance.",
        "ORDINAL" : "Rankings like first, second etc.",
        "CARDINAL"	: "Numerals."
        },orient='index')
    df = df.reset_index()
    df = df.rename(columns={'index':'Entity Tag',0:'Description'})
    return df.to_html(index=False,escape=False)
 
def make_clickable(s):
    return '<a target="_blank" href="{}">{}</a>'.format(s['Link'],s['Relation'])
 
def get_relation_table(G):
      relations = []
      for e in G.edges(data=True):
            relations.append({'Subject':e[0],'Object':e[1],'Relation':e[2]['relation'],'Link':e[2]['link']})
      df = pd.DataFrame(relations)
      df['Relation']=df.apply(make_clickable,axis=1)
      return df[['Subject','Relation','Object']].to_html(escape=False)