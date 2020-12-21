import plotly.graph_objects as go
import networkx as nx
import math

def addEdge(start, end, edge_x, edge_y,edge_z, lengthFrac=1, arrowPos = None, arrowLength=0.025, arrowAngle = 30, dotSize=20):
    """
    Used in "arrow_trace_creation" function
    # Adapted from #https://github.com/redransil/plotly-dirgraph
    # Start and end are lists defining start and end points
    # Edge x and y are lists used to construct the graph
    # arrowAngle and arrowLength define properties of the arrowhead
    # arrowPos is None, 'middle' or 'end' based on where on the edge you want the arrow to appear
    # arrowLength is the length of the arrowhead
    # arrowAngle is the angle in degrees that the arrowhead makes with the edge
    # dotSize is the plotly Scatter3d dot size you are using (used to even out line spacing when you have a mix of edge lengths)
    """
    # Get start and end cartesian coordinates
    x0, y0 = start
    x1, y1 = end
    
    # Incorporate the fraction of this segment covered by a dot into total reduction
    length = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )
    dotSizeConversion = .0565/20 # length units per dot size
    convertedDotDiameter = dotSize * dotSizeConversion
    lengthFracReduction = convertedDotDiameter / length
    lengthFrac = lengthFrac - lengthFracReduction
    
    # If the line segment should not cover the entire distance, get actual start and end coords
    skipX = (x1-x0)*(1-lengthFrac)
    skipY = (y1-y0)*(1-lengthFrac)
    x0 = x0 + skipX/2
    x1 = x1 - skipX/2
    y0 = y0 + skipY/2
    y1 = y1 - skipY/2
    
    # Append line corresponding to the edge
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None) # Prevents a line being drawn from end of this edge to start of next edge
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
    
    # Draw arrow
    if not arrowPos == None:
        
        # Find the point of the arrow; assume is at end unless told middle
        pointx = x1
        pointy = y1
        eta = math.degrees(math.atan((x1-x0)/(y1-y0)))
        
        if arrowPos == 'middle' or arrowPos == 'mid':
            pointx = x0 + (x1-x0)/2
            pointy = y0 + (y1-y0)/2
            
        # Find the directions the arrows are pointing
        signx = (x1-x0)/abs(x1-x0)
        signy = (y1-y0)/abs(y1-y0)
        
        # Append first arrowhead
        dx = arrowLength * math.sin(math.radians(eta + arrowAngle))
        dy = arrowLength * math.cos(math.radians(eta + arrowAngle))    
        edge_x.append(pointx)
        edge_x.append(pointx - signx**2 * signy * dx)
        edge_x.append(None)
        edge_y.append(pointy)
        edge_y.append(pointy - signx**2 * signy * dy)
        edge_y.append(None)
        
        # And second arrowhead
        dx = arrowLength * math.sin(math.radians(eta - arrowAngle))
        dy = arrowLength * math.cos(math.radians(eta - arrowAngle))    
        edge_x.append(pointx)
        edge_x.append(pointx - signx**2 * signy * dx)
        edge_x.append(None)
        edge_y.append(pointy)
        edge_y.append(pointy - signx**2 * signy * dy)
        edge_y.append(None)
    
    return edge_x, edge_y

def node_trace_creation(Graph, pos):
    """Creates the node coordinates. 1 coordinate for each node"""
    
    node_x = []
    node_y = []
    node_z = []
    for node in Graph.nodes():
        coor = pos[node]
        x = coor[0]
        y = coor[1]
        z = coor[2]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z = node_z,
        mode='markers + text',
        text = list(Graph.nodes()),
        hoverinfo='text + name',
        marker=dict(
            showscale=False,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlOrRd',
            reversescale=True,
            color=[node[1]["color"] for node in Graph.nodes(data=True)],
            size=15,
            line_width=0))
    
    return node_trace

def edge_trace_creation(Graph, pos):
    """Creates the edge coordinates. Note that there are 2 coordinates for each edge, the start and end"""
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in Graph.edges():
        coor0 = pos[edge[0]]
        x0 = coor0[0]
        y0 = coor0[1]
        z0 = coor0[2]
        coor1 = pos[edge[1]]
        x1 = coor1[0]
        y1 = coor1[1]
        z1 = coor1[2]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#000'),
        hoverinfo='none',
        mode='lines')
    
    return edge_trace

def edge_labels_creation(Graph, pos):
    """Labels each edge with the relation on the mid-point coordinate of the edge"""
    def midpoint(x1, y1, x2, y2, z1, z2):
        return ((x1 + x2)/2, (y1 + y2)/2, (z1 + z2)/2)

    mid_point_x = []
    mid_point_y = []
    mid_point_z = []
    for edge in Graph.edges():
        coor0 = pos[edge[0]]
        x0 = coor0[0]
        y0 = coor0[1]
        z0 = coor0[2]
        coor1 = pos[edge[1]]
        x1 = coor1[0]
        y1 = coor1[1]
        z1 = coor1[2]
        midpoint_coor = midpoint(x0, y0, x1, y1, z0, z1)
        mid_point_x.append(midpoint_coor[0])
        mid_point_y.append(midpoint_coor[1])
        mid_point_z.append(midpoint_coor[2])

    labels = list(nx.get_edge_attributes(Graph, 'relation').values())
    edge_trace_text = go.Scatter3d(x=mid_point_x, y=mid_point_y,z =mid_point_z,
                                   mode='markers+text',
                                   text=labels,
                                   textfont=dict(color="crimson"),
                                   #textposition='bottom center',
                                   marker={'symbol': 'circle', 'size': 5, 'color': "lightpink", 'line_width': 0},
                                   hoverinfo='text')
    return edge_trace_text
    
def arrow_trace_creation(Graph, pos):
    """Adds arrow-like visuals to the edges"""
    arrow_trace_x = []
    arrow_trace_y = []
    arrow_trace_z = []

    for edge in Graph.edges():
        coor0 = pos[edge[0]]
        x0 = coor0[0]
        y0 = coor0[1]
        coor1 = pos[edge[1]]
        x1 = coor1[0]
        y1 = coor1[1]
        # validation not the same node pointing to each other, such triples found
        if not (x0 == x1 and y0 == y1):
            arrow_trace_x, arrow_trace_y, arrow_trace_z = addEdge(coor0, coor1, arrow_trace_x, arrow_trace_y, 1, 'end', .02, 20, 10)

    arrow_trace = go.Scatter3d(x=arrow_trace_x, y=arrow_trace_y,z=arrow_trace_z, line=dict(width=1, color="black"), hoverinfo='none', mode='lines')
    return arrow_trace

def full_graph_creation(data):
    """
    # input eg. : [edge_trace, node_trace, edge_labels, arrow_trace]
    Based on components above, inserting those components you want.
    node_trace: node corrdinates and labels
    edge_trace: edge coordinates (optional)
    edge_labels: edge labels (optional)
    arrow_trace: adds arrow visual to make graph directed. Seems like plotly has no native support for this"""
    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )
    fig = go.Figure(data=data,
            layout=go.Layout(
                  width=1000,
                  height=1000,
                  showlegend=False,
                  scene=dict(
                   xaxis=dict(axis),
                   yaxis=dict(axis),
                   zaxis=dict(axis),
                  ),
                  margin=dict(t=1),
                  hovermode='closest'
                ))
    # removing the xaxis and yaxis post-creation of fig object. Not sure why does not work when doing it internally, but this approach works as well.
    # grid lines get removed together with the axis, cannot seem to have just grid lines
    fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
    fig.update_layout(xaxis_visible=False, xaxis_showticklabels=False)
    
    return fig 
    

def get_graph_fig3D(G):
    pos = nx.fruchterman_reingold_layout(G,dim=3)
    node_trace = node_trace_creation(G, pos)
    edge_trace = edge_trace_creation(G, pos)
    edge_labels = edge_labels_creation(G, pos)
    #arrow_trace = arrow_trace_creation(G, pos)
    fig = full_graph_creation([node_trace, edge_trace, edge_labels])
    return fig