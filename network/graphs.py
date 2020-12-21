import networkx as nx
import copy
import re

class FilterGraph():
  def __init__(self,G):
    self.G = copy.deepcopy(G)
    
  def filter_node(self,x):
    if self.sourceNode in x:
      return True
    if x in self.nodes:
      return True
    return False

  def get_closest_node_to_query(self,q):
    for n in self.G.nodes:
      if q in n:
        return n

  def updateNodes(self,x):
    node = self.get_closest_node_to_query(x)
    self.nodes = nx.algorithms.traversal.breadth_first_search.descendants_at_distance(self.G,node,1)

  def filter_nodes_by_number(self,x):
    if x==self.sourceNode:
      return True
    if x in self.nodes:
      if re.match(r'[0-9]',x):
        return True 
    return False

  def filter_by_source(self,sourceNode):
    self.sourceNode = sourceNode
    self.updateNodes(sourceNode)
    return nx.subgraph_view(self.G,filter_node=self.filter_node)
  
  
class CycleGraph():
  def __init__(self,cycle):
    self.cycle = cycle
    self.G = nx.DiGraph()
    for node in cycle:
          self.G.add_node(node)
    for i in range(len(cycle)-1):
          self.G.add_edge(cycle[i],cycle[i+1])
    self.G.add_edge(cycle[-1],cycle[0])
    
  def graph(self):
    return self.G   
      