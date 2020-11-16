import networkx as nx
import copy

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

  def filter_nodes_by_number(x):
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