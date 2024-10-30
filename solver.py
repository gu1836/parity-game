import time

from Vertex import Vertex
from parity_graph import Graph

#Zielonka’s algorithm
def solver_Iteration(graph):

    if graph.isNone():
        return [Graph([]),Graph([])]
   
    else:
        win = [Graph([]),Graph([])]
        maxP, playeri = graph.getAttractor()
        playerj = 1 - playeri
        #maxp:id,num
        arrtSet = graph.reach([maxP],playeri)
        #arrtset[id]
        g_remove_arrSet = graph.removeSubGraph(arrtSet)
        #g_remove:Graph
        win_1 = solver_Iteration(g_remove_arrSet)
        
        if win_1[playerj].isNone():
            win[playeri] = graph
            
        else:
            win_1_j_id = win_1[playerj].getIdList()
            
            reachWj = graph.reach(win_1_j_id,playerj)
            g_remove_wj = graph.removeSubGraph(reachWj)

            win_2 = solver_Iteration(g_remove_wj)
            win[playeri] = win_2[playeri]
            win[playerj] = graph.removeSubGraph(win[playeri].getIdList())

    
        return win
    


def solver_Dominion(graph):
    if graph.isNone():
        return [Graph([]),Graph([])]
    
    elif graph.isSingle_parity():

        solution = [Graph([]),Graph([])]
        maxP, playeri = graph.getAttractor()
        solution[playeri] = graph
        return solution
    
    else:
        win = [Graph([]),Graph([])]
        n = graph.get_graphSize()
        l = int((2*n)**0.5)
        dominio,playeri = graph.dominio(l)
        if not playeri == -1:
            playerj = 1 - playeri
            reachD = graph.reach(dominio,playeri)
            win_1 = solver_Dominion(graph.removeSubGraph(reachD))
            win[playerj] = win_1[playerj]
            win_1_j = win_1[playerj].getIdList()
            win[playeri] = graph.removeSubGraph(win_1_j)
        else:
            win = solver_Iteration(graph)
        
        return win



    





