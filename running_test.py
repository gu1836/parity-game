import time

from Vertex import Vertex
from parity_graph import Graph
from ramdon_graph import generate_graph
from ramdon_graph import domino_graph
from ramdon_graph import num_edge_graph

from input_graph import input_graph
from input_graph import read_Graph

from solver import solver_Iteration
from solver import solver_Dominion


def AlgorithmEfficiencyComparison(sizeRange):
    
    time_Iteration = 0
    time_Dominion = 0

    for i in range(100):
        
        graph = generate_graph(sizeRange)
        #running time for solver_Iteration
        start_time = time.time()
        sulotion_I = solver_Iteration(graph)  
        end_time = time.time()  
        elapsed_Iteration = end_time - start_time
        time_Iteration += elapsed_Iteration

        start_time = time.time()
        solution_D = solver_Dominion(graph)  
        end_time = time.time()  
        elapsed_Dominion = end_time - start_time
        time_Dominion += elapsed_Dominion


    return sizeRange, time_Iteration/100, time_Dominion/100

def single_winner_test(sizeRange):
    for i in range(5,sizeRange,50):
        table = []
        n = 10000
        only_winner_i = 0
        only_winner_t = 0
        only_winner_d = 0
        size = i
        for j in range(n):
            g = generate_graph(size)
            g_t = domino_graph(size, int(size/3), int(size/3),True)
            g_d = domino_graph(size, int(size/3), int(size/3))
            
            solution = solver_Dominion(g)
            solutionG = solver_Dominion(g_t)
            solutionD = solver_Dominion(g_d)
            
            if solution[0].get_graphSize() == 0 or solution[0].get_graphSize() == size:
            
                only_winner_i += 1
            if solutionG[0].get_graphSize() == 0 or solutionG[0].get_graphSize() == size:
            
                only_winner_t += 1
            
            if solutionD[0].get_graphSize() == 0 or solutionD[0].get_graphSize() == size:
            
                only_winner_d += 1
        #print([i,only_winner_i/n, only_winner_t/n, only_winner_d/n])
        table.append([i,only_winner_i/n, only_winner_t/n, only_winner_d/n])
    return table

  
def AlgorithmEfficiencyComparison_edge(graphSize):
    table = []

    for i in range(2,20,2):
        time_Iteration = 0
        time_Dominion = 0
        for j in range(10):
            graph = num_edge_graph(graphSize, i)
            start_time = time.time()
            sulotion_I = solver_Iteration(graph)  
            end_time = time.time()  
            elapsed_Iteration = end_time - start_time
            time_Iteration += elapsed_Iteration

            start_time = time.time()
            sulotion_D = solver_Dominion(graph)
            end_time = time.time()  
            elapsed_Dominion = end_time - start_time
            time_Dominion += elapsed_Dominion
        
        table.append([i,time_Iteration/10,time_Dominion/10])
    return table

def dominrangImproveComparison(graphSize,i_closed=False):
    table = []
    for i in range(10,101,10):
        time_Iteration = 0
        time_Dominion = 0
        for j in range(20):
            graph = domino_graph(graphSize, 10,i,i_closed)
            start_time = time.time()
            sulotion_I = solver_Iteration(graph)  
            end_time = time.time()  
            elapsed_Iteration = end_time - start_time
            time_Iteration += elapsed_Iteration

            start_time = time.time()
            sulotion_D = solver_Dominion(graph)
            end_time = time.time()  
            elapsed_Dominion = end_time - start_time
            time_Dominion += elapsed_Dominion
        print([i,time_Iteration/20,time_Dominion/20])
        table.append([i,time_Iteration/20,time_Dominion/20])
    return table

def dominSizeImproveComparison(graphSize,i_closed=False):
    table = []
    for i in range(10,101,10):
        time_Iteration = 0
        time_Dominion = 0
        for j in range(20):
            graph = domino_graph(graphSize, i,20,i_closed)
            start_time = time.time()
            sulotion_I = solver_Iteration(graph)  
            end_time = time.time()  
            elapsed_Iteration = end_time - start_time
            time_Iteration += elapsed_Iteration

            start_time = time.time()
            sulotion_D = solver_Dominion(graph)
            end_time = time.time()  
            elapsed_Dominion = end_time - start_time
            time_Dominion += elapsed_Dominion
        #print([i,time_Iteration/20,time_Dominion/20])
        table.append([i,time_Iteration/20,time_Dominion/20])
    return table


def dominranggraphEdge(graphSize,i_closed=False):
    table = []
    for i in range(10,101,10):

        edgenum = 0
        for j in range(20):
            graph = domino_graph(graphSize, 10,i,i_closed)
            edge = graph.getEdge()
            edgenum = 0
            for e in edge:
                edgenum += len(edge[e])
            
    return table


while True:
    print("Please select a function to run:")
    print("1. AlgorithmEfficiencyComparison")
    print("2. single_winner_test")
    print("3. AlgorithmEfficiencyComparison_edge")
    print("4. dominrangImproveComparison")
    print("5. dominSizeImproveComparison")
    print("6. dominranggraphEdge")
    print("7. Print Graph")
    print("0. Exit")

    choice = input("Enter your choice (0-7): ")
    if choice in ["1","2","3","4","5","6"]:
        result = []
        fileTitle = "?"
        txtname = input("Write into which file: ") + ".txt"
    if choice == "1":
        fileTitle = "Comparison of algorithm times for different graph sizes: "
        sizeRange = int(input("Enter size range: "))

        result = AlgorithmEfficiencyComparison(sizeRange)



    elif choice == "2":
        fileTitle = "Probability of occurrence of single-winner graph"
        sizeRange = int(input("Enter size range: "))

        result = single_winner_test(sizeRange)
        
        

    elif choice == "3":
        fileTitle = "The effect of the number of edges in the graph on efficiency"
        graphSize = int(input("Enter graph size: "))
       
        result = AlgorithmEfficiencyComparison_edge(graphSize)
        

    elif choice == "4":
        fileTitle = "The effect of the number of small cycle in the graph on efficiency"
        graphSize = int(input("Enter graph size: "))
        i_closed = int(input("Enter True or False for i_closed: (use 0 let Ture and anything else for False)"))
        if i_closed == 0:
            i = True
            fileTitle += " (the cycle is i-dominion)"
        else:
            fileTitle += " (the cycle only i-closed)"
            i = False
        result = dominrangImproveComparison(graphSize, i)
        

    elif choice == "5":
        fileTitle = "The effect of the size of cycle in the graph on efficiency"
        graphSize = int(input("Enter graph size: "))
        i_closed = int(input("Enter True or False for i_closed: (use 0 let Ture and anything else for False)"))
        if i_closed == 0:
            i = True
            fileTitle += " (the cycle is i-dominion)"
        else:
            fileTitle += " (the cycle only i-closed)"
            i = False
        result = dominSizeImproveComparison(graphSize, i)
        

    elif choice == "6":
        fileTitle = "The effect of the number of cycle to edges number in graph"
        graphSize = int(input("Enter graph size: "))
        i_closed = int(input("Enter True or False for i_closed: (use 0 let Ture and anything else for False)"))
        if i_closed == 0:
            i = True
        else:
            i = False

        result = dominranggraphEdge(graphSize, i)

    elif choice == "7":
        graphFrom = input("Input file source: t for typing, any other case for reading from file: ")
        if graphFrom == "t":
            graph = input_graph()
        else:
            filename = input("Enter the name of the file you want to print: ")
            graph = read_Graph(filename)
        
        graph.printG()
        
    
    elif choice == "0":
        break
    
    
    else:
        print("Invalid choice. Please try again.")
    
    if choice in  ["1","2","3","4","5","6"]:
        with open(txtname, 'w') as f:
                f.write(fileTitle + "\n")
                for i in result:
                    f.write(f"{i}\n")
    print("done")
