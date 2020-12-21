import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud
import streamlit as st
import plotly.graph_objs as go
import random

@st.cache(allow_output_mutation=True)
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
  
def plot3d(S,sourceNode=None):
  kk = nx.spring_layout(S,dim=3,scale=30)
  Xn=[kk[k][0] for k in S.nodes]# x-coordinates of nodes
  Yn=[kk[k][1] for k in S.nodes]# y-coordinates
  Zn=[kk[k][2] for k in S.nodes]# z-coordinates
  colour = []
  sizes = []
  colour = []
  count_by_node = {}
  Xe=[]
  Ye=[]
  Ze=[]
  for e in S.edges:
      Xe+=[kk[e[0]][0],kk[e[1]][0], None]# x-coordinates of edge ends
      Ye+=[kk[e[0]][1],kk[e[1]][1], None]
      Ze+=[kk[e[0]][2],kk[e[1]][2], None]
      try: 
        count_by_node[e[0]]+=4
      except:
        count_by_node[e[0]]=2
  for n in S.nodes:
    if n in count_by_node:
      sizes.append(min(count_by_node[n],20))
    else:
      sizes.append(10)
  i = 0
  for n in S.nodes:
    if sourceNode and sourceNode in n:
      colour.append('red')
    elif sizes[i]>10:
      colour.append('yellow')
    else:
      colour.append('blue')   
    i +=1  
  trace1=go.Scatter3d(x=Xe,
                y=Ye,
                z=Ze,
                mode='lines',
                line=dict(color='rgb(125,125,125)', width=1),
                hoverinfo='none'
                )

  trace2=go.Scatter3d(x=Xn,
                y=Yn,
                z=Zn,
                mode='markers',
                name='actors',
                marker=dict(symbol='circle',
                              size=sizes,
                              color=colour,
                              colorscale='Viridis',
                              line=dict(color='rgb(50,50,50)', width=3)
                              ),
                text=list(S.nodes),
                hoverinfo='text'
                )

  axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

  layout = go.Layout(
          width=1000,
          height=1000,
          showlegend=False,
          scene=dict(
              xaxis=dict(axis),
              yaxis=dict(axis),
              zaxis=dict(axis),
          ),
      margin=dict(
          t=1
      ),
      hovermode='closest',
     )
  data=[trace1, trace2]
  fig=go.Figure(data=data, layout=layout)
  return fig   

def plot_cycle(S):
  kk = nx.circular_layout(S,dim=3,scale=30)
  Xn=[kk[k][0] for k in S.nodes]# x-coordinates of nodes
  Yn=[kk[k][1] for k in S.nodes]# y-coordinates
  Zn=[kk[k][2] for k in S.nodes]# z-coordinates
  colour = []
  sizes = []
  colour = []
  Xe=[]
  Ye=[]
  Ze=[]
  for e in S.edges:
      Xe+=[kk[e[0]][0],kk[e[1]][0], None]# x-coordinates of edge ends
      Ye+=[kk[e[0]][1],kk[e[1]][1], None]
      Ze+=[kk[e[0]][2],kk[e[1]][2], None]
  trace1=go.Scatter3d(x=Xe,
                y=Ye,
                z=Ze,
                mode='lines',
                line=dict(color='rgb(125,125,125)', width=1),
                hoverinfo='none'
                )
  colours = []
  for n in S.nodes:
        colours.append(random.choice(['blue','red','orange','yellow','green']))
  trace2=go.Scatter3d(x=Xn,
                y=Yn,
                z=Zn,
                mode='markers',
                name='actors',
                marker=dict(symbol='circle',
                              size=10,
                              color=colours,
                              colorscale='Viridis',
                              line=dict(color='rgb(50,50,50)', width=3)
                              ),
                text=list(S.nodes),
                hoverinfo='text'
                )

  axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

  layout = go.Layout(
          width=1000,
          height=1000,
          showlegend=False,
          scene=dict(
              xaxis=dict(axis),
              yaxis=dict(axis),
              zaxis=dict(axis),
          ),
      margin=dict(
          t=1
      ),
      hovermode='closest',
     )
  data=[trace1, trace2]
  fig=go.Figure(data=data, layout=layout)
  return fig   