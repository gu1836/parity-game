from graphviz import Digraph
from Vertex import Vertex

#graph
#not change the vertex
#According to vertex produce the path
class Graph:
    def __init__(self, nodes, cycles=[], checkCycle=False):
        self.nodes = nodes#List of vertex
        self.idList = []
        self.priority = {}
        for i in self.nodes:
            self.idList.append(i.getId())
            self.priority[i.getId()] = i.getPriority()
        self.graphSize = len(self.nodes)
        self.checkCycle = checkCycle

        #According to the node list
        self.pointTo = {}
        self.pointFrom = {}
        self.produceEdge()
        
        self.cycles = cycles

    def printG(self,filename="graph"):
        dot = Digraph(comment='Parity Game')
        
        for i in range(len(self.nodes)):
            
            verexId = self.idList[i]
            shape = 'circle' if self.nodes[i].getPlayer() == 0 else 'square'
            dot.node(str(verexId), label=str(self.priority[verexId]), shape=shape)
            for next_id in self.pointTo[self.idList[i]]:
                dot.edge(str(self.idList[i]), str(next_id))
        dot.render(filename,format='jpg', view=True, engine='neato')

    
    def printGID(self,filename="graph_ID"):
        dot = Digraph(comment='Parity Game')
        
        for i in range(len(self.nodes)):
            
            verexId = self.idList[i]
            shape = 'circle' if self.nodes[i].getPlayer() == 0 else 'square'
            dot.node(str(verexId), label=str(verexId), shape=shape)
            for next_id in self.pointTo[self.idList[i]]:
                dot.edge(str(self.idList[i]), str(next_id))
        dot.render(filename,format='jpg', view=True, engine='neato')

    
    def printGM(self,p=[],c='red',filename='show'):#used to mark some specific vertexes in graph
        dot = Digraph(comment='Parity Game')
        
        for i in range(len(self.nodes)):
            
            verexId = self.idList[i]
            shape = 'circle' if self.nodes[i].getPlayer() == 0 else 'square'
            color = c if verexId in p else 'black'
            dot.node(str(verexId), label=str(self.priority[verexId]), shape=shape, color=color)
            for next_id in self.pointTo[self.idList[i]]:
                if verexId in p and next_id not in p:
                    style = 'dashed'
                elif verexId not in p and next_id in p:
                    style = 'dashed'
                else:
                    style = 'solid'
                dot.edge(str(self.idList[i]), str(next_id),style = style)
        dot.render(filename,format='jpg', view=True, engine='neato')

    def printSolution(self,win_solution,filename = "graph_soultion"):
        
        player0_node = win_solution[0].getIdList()
        player1_node = win_solution[1].getIdList()
        player_path = [win_solution[0].getEdge(),win_solution[1].getEdge()]
        dot = Digraph(comment='Parity Game Solution')
        for i in range(len(self.idList)):
            if self.idList[i] in player0_node:
                player = 0
            elif self.idList[i] in player1_node:
                player = 1
            verexId = self.idList[i]
            shape = 'circle' if self.nodes[i].getPlayer() == 0 else 'square'
   
            color = 'red' if player == 0 else 'blue'
            dot.node(str(verexId), label=str(self.priority[verexId]), shape=shape, color=color)
            for next_id in self.pointTo[self.idList[i]]:
                if next_id in player_path[player]:
                    style = 'solid'
                else:    
                    style = 'dashed'

                dot.edge(str(self.idList[i]), str(next_id), style = style)
        dot.render(filename,format='jpg', view=True, engine='neato')



    def write_Graph(self, filename):

        with open(filename+".txt", 'w') as f:
            #f.write(f"len(self.idList)\n")
            for i in self.nodes:
                id = i.getId()
                player = i.getPlayer()
                priority = i.getPriority()
                pointsto = " ".join(str(j) for j in self.pointTo[id])
                f.write(f"{id} {player} {priority} {pointsto}\n")


    def get_nodes(self):#unit test√
        return self.nodes

    def get_graphSize(self):#unit test√
        return self.graphSize
        
    def getIdList(self):#unit test√
        #used to check and positioning the vertex form self.nodes
        return self.idList

    def getEdge(self):#unit test√
        return self.pointTo    

    def isNone(self):#unit test√
        return self.graphSize == 0
    
    def isSingle_parity(self,node=[]):#unit test√

        if len(node) == 0:
            node = self.idList
        
        parity = self.priority[node[0]]%2
        result = True
        for n in node:
            if self.priority[n]%2 != parity:
                return False
                

        return result
    
    
    def isSingle_player(self,nodes=[]):#unit test√
        if len(nodes) == 0:
            vertexes = self.nodes
        else:
            vertexes = []
            for i in nodes:
                vertex = self.nodes[self.idList.index(i)]
                vertexes.append(vertex)
        player = vertexes[0].getPlayer()
        for v in vertexes:
            if not v.getPlayer() == player:
                return False, -1

        return True, player


    def produceEdge(self):#unit test√
        #By reading the point to list for each vertex
        #the vertex point to and vertex point from are recorded separately.

        for id in self.idList:
            self.pointFrom[id] = []      

        for node in self.nodes:
            #update self.pointto
            pointToInit = node.getPointTo()
            pointTo = []
            for i in pointToInit:

                if i in self.idList:
                    #update point To
                    pointTo.append(i)
                    #update Point From
                    self.pointFrom[i].append(node.getId())
                                           
            self.pointTo[node.getId()] = pointTo



    def getAttractor(self):#unit test√
        #find the vertex that have the max priority

        maxPriority = max(self.priority.values())
        maxPriorityID = list(self.priority.keys())[list(self.priority.values()).index(maxPriority)]
        
        return maxPriorityID, maxPriority%2
    
    def reach(self, attrSet, winner):#unit test√
        nodes = self.nodes
        attrSetId = attrSet
        pointToAttr = attrSet
        
        pointToAttr = list(set(pointToAttr))
        SetCanExpand = True 
        while SetCanExpand:
            #SetCanExpand = False
            nextLevel = []
            for pre in pointToAttr:
                choice = self.pointFrom[pre]
                
                for i in choice:
                    if i not in attrSetId:
                        vertex = nodes[self.idList.index(i)]
                        player = vertex.getPlayer()

                        if player == winner:

                            attrSetId.append(i)
                            nextLevel.append(i)
                        else:
                            leaveWay = [l for l in self.pointTo[i] if l not in attrSetId]
                            
                            if len(leaveWay) == 0:
                                attrSetId.append(i)
                                nextLevel.append(i)
            
            if nextLevel:
                pointToAttr = nextLevel
            else:
               SetCanExpand = False 
                
        return attrSetId
    
    def removeSubGraph(self, remove_List_id):#unit test√
        #used to remove node set and generate a new graph
        newNodes = []
        connect = []
        
        for i in self.idList:
        
            if i not in remove_List_id:
                newNodes.append(self.nodes[self.idList.index(i)])
        

        #remove the connect and disconnect set which contains the node need to be removed,
        #and add the new list as the element for the new sub graph
        if self.checkCycle:
            for c in self.cycles:
                if len(c) + len(remove_List_id) == len(set(c + remove_List_id)):
                    connect.append(c)
            return Graph(newNodes, connect, True)
        else:
            return Graph(newNodes)


           
    def dominio(self, l):

        #used to find the small dominio which size not bigger than l
        #small dominio:
        #1. this subGraph is i_closed(i.e player ¬i can not leave this subGraph if player i not leave this)
        #2. player i can really win in this graph(i.e. the bigest priority counterpart player i)

        if not self.checkCycle :
            #if list connect and list disconnect both empty, that means the graph is not a subgraph 
            #which is generate by the  removeSubGraph function
            #acroding to the removesubgraoh function
            #There is one and only one case where both connect and disconnect are empty
            #other than the case where the graph first calls the function 
            #check the combination if the node in the set can be connect 
            totalCycle = self.subCycles(l)
            self.cycles = totalCycle
            
        else:
            totalCycle = self.cycles


        dominio = []
        totalCycle.sort(key = lambda i:len(i),reverse=True)
        
        for i in totalCycle:
                
            closedReust, win_set = self.is_i_dominion(i)
            if len(win_set) == 0:
                win_set = i
            if closedReust[0]:

                if self.playerWin(i,0):
                    dominio = win_set
                    
                    return dominio,0
            elif closedReust[1]:

                if self.playerWin(i,1):
                    dominio = win_set
                    
                    return dominio,1
            else:
                self.cycles.remove(i)
                
        
        return [],-1
    
    def is_i_dominion(self, nodes):#unit test√
        #The conditions of i-closed cycle
        #1.for player i, there is not node for player -i can point to the node out of set
        #2.for player i, there is at least one node point to the set
        #Assume for a moment that this small graph is 0_closed and 1_closed
        #this list is used to recored if any node for player -i point to the node out of set
        playeri = [True,True]
        isS_p,p = self.isSingle_player(nodes)
        if isS_p:
            #playerNoti[1-p] = False
            playeri[1-p] = False
        maxPriority = 0
        
        for n in nodes:
            if self.priority[n] > maxPriority:
                maxPriority = self.priority[n]
            vertex = self.nodes[self.idList.index(n)]
            player = vertex.getPlayer()
            #if there is a player i node can point to node out of set
            #It has been shown that nodes is not ¬i_closed
            #so skip this node
            playeri_pointTo = False
            for i in self.pointTo[n]:
                if playeri[1 - player] and i not in nodes:
                    #if the next node i point to other node out of the set
                    #that means player ¬i can not control the token never leaving the area
                    #break this for loop and check next node in nodes
                    playeri[1 - player] = False
                
                if playeri[player] and not playeri_pointTo and i in nodes:
                    playeri_pointTo = True
            
            if not playeri_pointTo:
                playeri[player] = playeri_pointTo
            
            if  not playeri[0] and not playeri[1]:
                return [False,False],[]

            
        #i_closed = [playerNoti[0] and playeri[0],playerNoti[1] and playeri[1]]
        #check the maxPriority
        winner_i = maxPriority%2
        if playeri[1-winner_i]:
            playeri[1-winner_i] = False
        if playeri[winner_i]:
            
            #Make sure there are no smaller winning sets belonging to palyer j in this cycle
            subcycle = self.subCycles(len(nodes)-1,nodes)
            
            #subcycle = self.subCycles(len(nodes),nodes)
            for c in subcycle:
                c_dominion, subC = self.is_i_dominion(c)
                
                if c_dominion[1-winner_i]:
                    
                    return c_dominion, subC
                
            
            return playeri,nodes
        
        else:
            return [False,False],[]
        
        
    def playerWin(self, nodes,player):#unit √
        #used to check if a small graph is i_closed cycle and player i can win the game by control the token never leave the subGraph

        if self.isSingle_parity(nodes):
            priority = self.priority[nodes[0]]
            return priority%2 == player

        maxPriority = 0
        for i in nodes:
            priority = self.priority[i]
            if priority > maxPriority:
                maxPriority = priority

        return maxPriority%2 == player         




    def is_i_closed(self, nodes):#unittest√
        #The conditions of i-closed cycle
        #1.for player i, there is not node for player -i can point to the node out of set
        #2.for player i, there is at least one outgoing edge point to vertex in set for each vertex
        #Assume for a moment that this small graph is 0_closed and 1_closed
        #this list is used to recored if any node for player -i point to the node out of set
        #playerNoti = [True,True]
        #this list is used to recored if there are node for player i can point to the node in the set
        playeri = [True,True]
        isS_p,p = self.isSingle_player(nodes)
        if isS_p and len(nodes) > 1:
            #playerNoti[1-p] = False
            playeri[1-p] = False
            

        for n in nodes:
            vertex = self.nodes[self.idList.index(n)]
            player = vertex.getPlayer()
            #if there is a player i node can point to node out of set
            #It has been shown that nodes is not ¬i_closed
            #so skip this node
            playeri_pointTo = False
            for i in self.pointTo[n]:
                if playeri[1 - player] and i not in nodes:
                    #if the next node i point to other node out of the set
                    #that means player ¬i can not control the token never leaving the area
                    #break this for loop and check next node in nodes
                    playeri[1 - player] = False
                
                if playeri[player] and not playeri_pointTo and i in nodes:
                    playeri_pointTo = True
            
            if not playeri_pointTo:
                playeri[player] = playeri_pointTo
            
            if  not playeri[0] and not playeri[1]:
                return [False,False]

        return playeri
    


    def subCycles(self, l, checkSet=[]):#unit test√
        #cycles means the token can come back to the node it start from for each node in this subset
        #Consider function playerWin
        #toekn in this set should have one and only one path to go through the whole subset
        #this funcion's input is a node as the start node,and the max range of the cycle
        #it will retrun a list that contains all one-way loops of length up to max range
        #use DFS find the cycle
        #For each node, a DFS search is performed starting from it and the search path is recorded during the search.
        #When a node that has already been visited is accessed, 
        #check if the search path contains a loop and if so, add the loop to the list of loops.


        if len(checkSet) == 0:
            checkSet = self.idList
        
        visited = set()
        cycles = []

        def dfs(node, path):
            visited.add(node)
            for neighbor in self.pointTo[node]:
                if neighbor not in visited and neighbor in checkSet:
                    dfs(neighbor, path + [neighbor])
                elif neighbor in path:
                    cycle = path[path.index(neighbor):]
                    if cycle not in cycles:
                        cycles.append(cycle)

        for node in checkSet:
            dfs(node, [node])
    
        return [cycle for cycle in cycles if len(cycle) <= l]

    
            
    def graphConnect(self,idSet=[]):#unit test√
        #Used to determine if the generated graph is complete
        #check if every node is connect with each other
        #if yes,retrun true
        #else, retrun false and each split subgraph
        #it also can used to check if node of set in graph can connect to each other 
        # or they are separate parts that cannot be connected

        subGraph = []
        subIdSet = []
        if len(idSet) == 0:
            idSet = self.idList

        connect_nodes = self.nodeNetwork(idSet)
        
        

        if len(connect_nodes) == len(idSet):
            return True, [idSet]
        
        else:
            subGraph.append(connect_nodes)
            subIdSet += connect_nodes
            checkAgain = True
            while checkAgain:

                otherNode = [i for i in idSet if i not in subIdSet]

                new_subSet = self.nodeNetwork(otherNode)
                if len(new_subSet) == len(otherNode):
                    subGraph.append(new_subSet)
                    checkAgain = False
                else:
                    subGraph.append(new_subSet)
                    subIdSet += new_subSet
                    
            
            return False, subGraph
    
    def nodeNetwork(self, checkRange=[]):#unit test√
        #Breadth-first search
        #Used to find the set of all nodes connect with a node in a given check range

        #If no check range is given, the default check range is the whole graph
        if len(checkRange) == 0:
            nodes = self.idList
        else:
            nodes = checkRange

        # Check if all nodes are in graph
        for node in nodes:
            
            if not node in self.idList:
                return []
        
        #Select the first one from the node list and start stretching
        connect_nodes = [nodes[0]]
        need_check = True
        #check list will be update when all possible expansions are marked
        checkList = connect_nodes

        while need_check:
            new_checkList = []
            #check every node in check list, 
            #Add their extension node to new_checkList as the checklist for the next layer of checks
            for node in checkList:
                #Get the pointTo list and pointFrom list of the current node 
                #rmoves the node that have been visitde
                #and which are not in the nodes list (i.e. those that need to be checked for links)
                pointTo = [i for i in self.pointTo[node] if i in nodes and i not in connect_nodes]
                new_checkList += pointTo
                pointFrom =  [i for i in self.pointFrom[node] if i in nodes and i not in connect_nodes]
                new_checkList += pointFrom
            
            #Ending the loop without the next layer of extension
            if len(new_checkList) == 0:
                need_check = False
            else:
                #Make a new checklist of all the ids that appear in the new_checklist and continue the loop
                checkList = list(set(new_checkList))
                #and add this part of the id to the  conect_nodes list that have been confirmed to be linked
                connect_nodes += checkList
                    
        connect_nodes = list(set(connect_nodes))

        return connect_nodes
    


    def checkSolution(self, solution,player):#unit test √
        #Conditions to be met for solution:
        #1. solution is i-closed, if the node of solution cannot connect each other, each part is i-closed
        #2. as for each cycle in the solution, at least have one i-closed cycle have the biggest parity is belone i
        #3. as for other cycle which have the biggest cycle belone -i, it cannot be -i-closed
        if solution.get_graphSize() == 0:
            return self.checkSolution(Graph(self.nodes),1-player)
        for v in solution.get_nodes():
            if v not in self.nodes:
                return False
        
        solutionId = solution.getIdList()
        #check the number of part of solution:
        solutionConnect, solutionPart = self.graphConnect(solutionId)
        
        #if each node in solution can connect each other, check this set if is i-closed
        #else,check each part

        if solutionConnect:

            rightS = self.is_i_closed(solutionId)[player]
        
        else:
            rightS = True
            for part in solutionPart:
                if not self.is_i_closed(part)[player]:
                    rightS = False
                    break
        
        if not rightS:

            return False
               
        #find the i-closed cycle and check it's max parity
        #if it is the winning set for player i
        
        #if the cycle is -i-closed 
        #check if the max parity is not bleone to player -i

        #each part of solution at least have a i-closed and can win for i cycle

        for part in solutionPart:
            
            haveWinSet = False
            solutionCycles = self.subCycles(len(part),part)
            haveWinJ = False
            for cycle in solutionCycles:

                closed = self.is_i_closed(cycle)

                if closed[1 - player]:
                    
                    if self.playerWin(cycle, 1 - player):

                        haveWinJ = True
                
                if closed[player]:
                    
                    if self.playerWin(cycle,player):
        
                        haveWinSet = True

            if not haveWinSet or  haveWinJ:
    
                return False
            
        return True




