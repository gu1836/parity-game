from Vertex import Vertex
from parity_graph import Graph
import random
#Completely random graph
def generate_graph(graphSize):

    rangeP = ((graphSize//10)+1)*5
    vertexList = []
    for i in range(graphSize):
        player = random.randint(0,1)
        priority = random.randint(1,rangeP)
        
        pointTo = []
        addProbab = 0
        p = 0.8
        while addProbab < p :
            new_add = random.randrange(0,graphSize,1)
            pointTo.append(new_add)
            addProbab = random.random()
            p *= 0.5
        pointTo = list(set(pointTo))
        vertexList.append(Vertex(i,player,priority,pointTo))
    
    graph = Graph(vertexList)
    graph_connect, subGraph = graph.graphConnect()
    
    if graph_connect:
        return graph
    else:
        while not len(subGraph) == 1:
            subset = subGraph[0]
            connect_node = random.choice(subset)
            otherSet = [i for i in range(graphSize) if i not in subset]
            connect_node2 = random.choice(otherSet)
            connect = random.randint(0,1)
            if connect == 0:
                vertexList[connect_node].addPath(connect_node2)
            
            else:
                vertexList[connect_node2].addPath(connect_node)
            for i in range(1, len(subGraph)):
                lst = subGraph[i]
                if connect_node2 in lst:
                    subGraph[0] += lst
                    subGraph.remove(lst)
                    break

        
        return Graph(vertexList)

        #return newGraph


def domino_graph(graphsize, maxdominoSize, minDnum=1, winDomino=False):
    if graphsize < maxdominoSize:
        return Graph([])

    rangeP = ((graphsize//10)+1)*5
    domino_set = []
    vertexList = []
    vertexId = 0
    for i in range(minDnum):
        if maxdominoSize > graphsize - len(vertexList):
            maxdominoSize = graphsize - len(vertexList)
            
        if maxdominoSize == 0 :
            break
        elif maxdominoSize == 1:
            dominoSize = 1
        
        else:
            dominoSize = random.randint(1,maxdominoSize)
        domino_id = []
        if not winDomino:
            for j in range(dominoSize):
                vid = vertexId + j
                player = random.randint(0,1)
                priority = random.randint(1,rangeP)

                if j == dominoSize-1:
                    pointTo = [vertexId]
                else:
                    pointTo = [vertexId+j+1]
                domino_id.append(vid)
                vertexList.append(Vertex(vid,player,priority,pointTo))
        
        #To ensure that the loop is i-closed and that only player i is the winner
        #Given that each node within the loop may be added to a new out put,
        #the loop will consist entirely of nodes belonging to player i
        #Also, to ensure that player i can win within this loop, 
        #the set will be a single parity and belong to i
        else:
            player = random.randint(0,1)
            priorityRange = [i for i in range(1,rangeP) if i%2 == player]
            for j in range(dominoSize):
                vid = vertexId + j
                priority = random.choice(priorityRange)

                if j == dominoSize-1:
                    pointTo = [vertexId]
                else:
                    pointTo = [vertexId+j+1]
                domino_id.append(vid)
                vertexList.append(Vertex(vid,player,priority,pointTo))


        domino_set.append(domino_id)
        vertexId = len(vertexList)
    
    #Completing a node other than domino
    for i in range(vertexId,graphsize):
        player = random.randint(0,1)
        priority = random.randint(1,rangeP)
        
        pointTo = []
        addProbab = 0
        p = 0.8
        while addProbab < p :
            new_add = random.randrange(0,graphsize,1)
            pointTo.append(new_add)
            addProbab = random.random()
            p *= 0.5
        pointTo = list(set(pointTo))
        vertexList.append(Vertex(i,player,priority,pointTo))

    graph = Graph(vertexList)

    graph_connect, subGraph = graph.graphConnect()
    if graph_connect:
        return graph
    else:
        #because of the cycle make before
        #It doesn't change the fact that these nodes can form loops
        #if add a new pointTo to some node in the subgraph
        #it will only make the subgraph become not i-closed
        #the i is other player for the node who add a new pointTo
        #as for the node is point from other, that can not change any for the cycle
        #the only things will broken the i-domion,
        #Two nodes belonging to different players in the subgraph are added to the edge at the same time
        #so it different for the generate_graph function,
        #as add the pointTo, this funcion will control that each cycle have only one node can add pointTo
        #so that this function recored each dominion.
        domino_add_edge = []
        while not len(subGraph) == 1:
            subset = [i for i in subGraph[0] if i not in domino_add_edge]
            otherSet = [i for i in range(graphsize) if i not in subGraph[0]]

            if len(subset) == 0:
                #the subgraph in subgraph[0] is one or more cycle connect eachother
                #and each cycle already have node point out of the cycle
                #so the add path progroress is node in otherset -> cycle
                connect_node = random.choice(subGraph[0])
                connect_node2 = random.choice(otherSet)
                vertexList[connect_node2].addPath(connect_node)
            else:
                connect_node = random.choice(subset)
                connect_node2 = random.choice(otherSet)
                #only add point to edge
                vertexList[connect_node].addPath(connect_node2)
            #add new subgraph into out put set
            for i in range(1, len(subGraph)):
                lst = subGraph[i]
                if connect_node2 in lst:
                    subGraph[0] += lst
                    subGraph.remove(lst)
                    break
            #add the domino who had been add point to into the set domino_add_edge
            #and node in domino_add_edge will not be add new point to edge
            for d in domino_set:
                if connect_node in d:
                  domino_add_edge += d 
                  domino_set.remove(d)
                  break 
        
        return Graph(vertexList)

def num_edge_graph(graphSize,  outgoing):
    rangeP = ((graphSize//10)+1)*5
    vertexList = []
    id_list = [i for i in range(graphSize)]
    for i in range(graphSize):
        player = random.randint(0,1)
        priority = random.randint(1,rangeP)
        
        pointTo = random.sample(id_list,outgoing)
       
        vertexList.append(Vertex(i,player,priority,pointTo))
    
    graph = Graph(vertexList)
    graph_connect, subGraph = graph.graphConnect()
    
    if graph_connect:
        return graph
    else:
        while not len(subGraph) == 1:
            subset = subGraph[0]
            connect_node = random.choice(subset)
            otherSet = [i for i in range(graphSize) if i not in subset]
            connect_node2 = random.choice(otherSet)
            connect = random.randint(0,1)
            if connect == 0:
                vertexList[connect_node].changePath(connect_node2)
            
            else:
                vertexList[connect_node2].changePath(connect_node)
            for i in range(1, len(subGraph)):
                lst = subGraph[i]
                if connect_node2 in lst:
                    subGraph[0] += lst
                    subGraph.remove(lst)
                    break

        
        return Graph(vertexList)


