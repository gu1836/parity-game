from Vertex import Vertex
from parity_graph import Graph

def input_graph():
    vertexs = []
    graphSize = int(input("Enter a number as the size of the graph you want "))

    for id in range(graphSize):
        print("for the node ", id)
        player = int(input("Enter 0 or 1 as the player of the node: "))

        while not player == 0 and not player == 1:
            player = int(input("Enter 0 or 1 as the player of the node x: "))
        priority = int(input("Enter a positive integer as the priority: "))

        pointTo = set()
        
        while True:
            condition = input("Enter id of node this node will point to or every non-numeric characters as a sign of finish:")
            if condition.isnumeric():
                next_id = int(condition)
                if next_id < graphSize and next_id >= 0:
                    pointTo.add(next_id)
                else:
                    print("Invalid vertex id")
            else:
                if len(pointTo) > 0:
                    break
                else:
                    print("each node at least have one out edge")
        
        vertexs.append(Vertex(id, player, priority,list(pointTo)))
    
    return Graph(vertexs)

def read_Graph(filename):
    with open(filename+".txt", 'r') as f:
        #n = int(f.readline())
        #print(n)
        lines = f.readlines()
        # Check file format
        if len(lines) == 0:
            raise ValueError('File is empty')

        vertexSet = []
        idSet = []
        for line in lines:
            
            
            data = line.strip().split()
            if len(data) <= 3:
                raise ValueError(f'vertex data Error(missing):{line}')
            try:
                for d in data:
                    int(d)
            except ValueError:
                raise ValueError(f'Invalid character in file: {line}')
            if int(data[1]) not in [0,1]:
                raise ValueError(f'Invalid player: {line}')
            if int(data[0]) in idSet:
                raise ValueError(f'Repeat vertex Id: {line.strip()} and {lines[idSet.index(int(data[0]))]}')


            pointTo = [int(data[i]) for i in range(3,len(data))]
            idSet.append(int(data[0]))
            vertex = Vertex(int(data[0]),int(data[1]), int(data[2]), pointTo)
            vertexSet.append(vertex)

        return Graph(vertexSet)


