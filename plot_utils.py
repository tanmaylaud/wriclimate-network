import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud

def plot(S):
  figure = plt.figure(figsize=(20,20))
  pos = nx.spring_layout(S)
  nx.draw(S, 
              pos, 
              edge_color='cyan',
              width=8,
              node_size=100, 
              node_color='seagreen',
              alpha=1,
              edge_cmap=plt.cm.Blues,
              font_size=20,
              labels={node: node for node in S.nodes()}
              )   
  plt.axis('off')
  return figure

def plot_cloud(ranks,max_nodes=20):
    figure = plt.figure(figsize=(20,20))
    wc = WordCloud(width=3000,height=1500,relative_scaling=1,background_color="white")
    plt.imshow(wc.generate_from_frequencies(frequencies=ranks[0][:max_nodes].to_dict()), interpolation='bilinear')
    plt.axis("off")
    return figure