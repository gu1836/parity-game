import unittest
from Vertex import Vertex
from parity_graph import Graph
from solver import solver_Iteration
from solver import solver_Dominion
from ramdon_graph import generate_graph

class TestVertex(unittest.TestCase):
    
    def setUp(self):
        self.vertex = Vertex(0, 1, 3, [1, 2])
        self.graphSize = 10
        
    def test_getId(self):
        self.assertEqual(self.vertex.getId(), 0)
        
    def test_getPlayer(self):
        self.assertEqual(self.vertex.getPlayer(), 1)
        
    def test_getPriority(self):
        self.assertEqual(self.vertex.getPriority(), 3)
        
    def test_getPointTo(self):
        self.assertEqual(self.vertex.getPointTo(), [1, 2])
        
    def test_winerFor(self):
        self.assertEqual(self.vertex.winerFor(), 1)
        
    def test_checkEdgeRange_true(self):
        self.assertTrue(self.vertex.checkEdgeRange(self.graphSize))
        
    def test_checkEdgeRange_false(self):
        v = Vertex(10, 1, 3, [11, 12])
        self.assertFalse(v.checkEdgeRange(self.graphSize))
        
    def test_addPath(self):
        self.vertex.addPath(3)
        self.assertEqual(self.vertex.getPointTo(), [1, 2, 3])
        
    def test_changePath(self):
        self.vertex.changePath(4)
        self.assertEqual(self.vertex.getPointTo(), [2, 4])
    
    def test_checkPlayer(self):
        with self.assertRaises(ValueError):
            Vertex(1, 2, 3, [1, 2])


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.v1 = Vertex(1, 0, 0, [2])
        self.v2 = Vertex(2, 1, 1, [3])
        self.v3 = Vertex(3, 0, 1, [4])
        self.v4 = Vertex(4, 1, 5, [1])

        self.vertices = [self.v1, self.v2, self.v3, self.v4]



    def test_write_Graph(self):
        graph = Graph(self.vertices)
        graph.write_Graph("test_graph")

        with open("test_graph.txt", "r") as f:
            data = f.readlines()

        self.assertEqual(len(data), 4)

        self.assertEqual(data[0].strip(), "1 0 0 2")
        self.assertEqual(data[1].strip(), "2 1 1 3")
        self.assertEqual(data[2].strip(), "3 0 1 4")
        self.assertEqual(data[3].strip(), "4 1 5 1")

    def test_get_nodes(self):
        graph = Graph(self.vertices)
        nodes = graph.get_nodes()

        self.assertEqual(len(nodes), 4)

        self.assertIn(self.v1, nodes)
        self.assertIn(self.v2, nodes)
        self.assertIn(self.v3, nodes)
        self.assertIn(self.v4, nodes)

    def test_get_graphSize(self):
        graph = Graph(self.vertices)
        graph_size = graph.get_graphSize()

        self.assertEqual(graph_size, 4)

    def test_getIdList(self):
        graph = Graph(self.vertices)
        id_list = graph.getIdList()

        self.assertEqual(len(id_list), 4)

        self.assertIn(1, id_list)
        self.assertIn(2, id_list)
        self.assertIn(3, id_list)
        self.assertIn(4, id_list)

    def test_isNone(self):
        empty_graph = Graph([])
        self.assertTrue(empty_graph.isNone())

        non_empty_graph = Graph(self.vertices)
        self.assertFalse(non_empty_graph.isNone())

    def test_checkPriority(self):
        with self.assertRaises(ValueError):
            Vertex(1, 0, -1, [1, 2])
        with self.assertRaises(ValueError):
            Vertex(1, 0, 1.5, [1, 2])
    
    def test_isSingle_parity(self):
        # Testing for single parity
        graph = Graph(self.vertices)

        self.assertFalse(graph.isSingle_parity())

        v1 = Vertex(1, 0, 6, [2])
        v2 = Vertex(2, 1, 0, [3])
        v3 = Vertex(3, 0, 2, [4])
        v4 = Vertex(4, 1, 4, [1])

        graph = Graph([v1, v2, v3, v4])
        self.assertTrue(graph.isSingle_parity())

    def test_isSingle_player(self):
        g_n_s_p = Graph(self.vertices)
        self.assertEqual(g_n_s_p.isSingle_player(),(False,-1))
        v1 = Vertex(1, 1, 6, [2])
        v2 = Vertex(2, 1, 0, [3])
        v3 = Vertex(3, 1, 2, [4])
        v4 = Vertex(4, 1, 4, [1])

        graph = Graph([v1, v2, v3, v4])
        self.assertEqual(graph.isSingle_player(),(True,1))

    

    def test_producePath(self):
        v1 = Vertex(1, 0, 6, [2])
        v2 = Vertex(2, 1, 0, [3])
        v3 = Vertex(3, 0, 2, [4])
        v4 = Vertex(4, 1, 4, [1])
        graph = Graph([v1, v2, v3, v4])
        self.assertEqual(graph.pointTo, {1:[2], 2:[3], 3:[4], 4:[1]})
        self.assertEqual(graph.pointFrom, {1:[4], 2:[1],3:[2],4:[3]})
    
    def test_getAttractor(self):
        graph = Graph(self.vertices)
        self.assertEqual(graph.getAttractor(),(4,1))
    
    def test_reach(self):
        v1 = Vertex(0,0,2,[3])
        v2 = Vertex(1,0,3,[2,4])
        v3 = Vertex(2,0,3,[2,5])
        v4 = Vertex(3,1,3,[0,1,4])
        v5 = Vertex(4,0,5,[3,5])
        v6 = Vertex(5,1,1,[4,2])
        graph = Graph([v1,v2,v3,v4,v5,v6])
        self.assertEqual(graph.reach([2],0),[2, 1])
        self.assertEqual(graph.reach([2],1),[2, 5])
    
    def test_removeSubGraph(self):
        g = Graph(self.vertices)
        g_r = g.removeSubGraph([1])
        #vertex number
        self.assertEqual(g_r.get_graphSize(),3)
        #right vertex
        self.assertTrue(self.v2 in g_r.get_nodes())
        self.assertTrue(self.v3 in g_r.get_nodes())
        self.assertTrue(self.v4 in g_r.get_nodes())
        #check edge
        self.assertEqual(g_r.getEdge()[2], [3])
        self.assertEqual(g_r.getEdge()[3], [4])
        self.assertEqual(g_r.getEdge()[4], [])
    
    def test_graphConnect(self):
        v1 = Vertex(0,0,0,[1])
        v2 = Vertex(1,0,1,[0])
        v3 = Vertex(2,0,2,[2,3])
        v4 = Vertex(3,1,3,[4])
        v5 = Vertex(4,1,4,[3])
        v6 = Vertex(5,1,5,[5])
        g_not_c = Graph([v1,v2,v3,v4,v5,v6])
        #not connect graph
        self.assertEqual(g_not_c.graphConnect(),(False, [[0, 1], [2, 3, 4], [5]]))
        #not connect sub-graph
        self.assertEqual(g_not_c.graphConnect([2,4]),(False, [[2],[4]]))
        #connect graph
        self.assertEqual(Graph(self.vertices).graphConnect(),(True,[[1,2,3,4]]))

    def test_playerWin(self):
        node1 = Vertex(1, 0,1,[2])
        node2 = Vertex(2, 1,2,[3])
        node3 = Vertex(3, 0,3,[4])
        node4 = Vertex(4, 1,4,[1])
        graph = Graph([node1, node2, node3, node4])
        self.assertTrue(graph.playerWin([1, 2], 0))
        self.assertFalse(graph.playerWin([1, 2], 1))
        self.assertTrue(graph.playerWin([1, 2, 3], 1))
        self.assertFalse(graph.playerWin([1, 2, 3], 0))
        self.assertFalse(graph.playerWin([1, 2, 3, 4], 1))
        self.assertTrue(graph.playerWin([1, 2, 3, 4], 0))

    def test_is_i_closed(self):
        graph = Graph(self.vertices)
        self.assertEqual(graph.is_i_closed([1,2,3,4]),[True,True])
        v1 = Vertex(0,0,2,[3])
        v2 = Vertex(1,0,3,[2,4])
        v3 = Vertex(2,0,2,[2,5])
        v4 = Vertex(3,1,3,[0,1])
        v5 = Vertex(4,1,4,[3,5])
        v6 = Vertex(5,1,1,[4,2])
        graph_6 = Graph([v1,v2,v3,v4,v5,v6])
        self.assertEqual(graph_6.is_i_closed([1,2]),[True,False])
        self.assertEqual(graph_6.is_i_closed([1,2,5]),[False,False])
        self.assertEqual(graph_6.is_i_closed([0]),[False,False])
        self.assertEqual(graph_6.is_i_closed([0,3]),[False,True])

    def test_nodeNetwork(self):
        v1 = Vertex(0,0,2,[1])
        v2 = Vertex(1,0,3,[0])
        v3 = Vertex(2,0,2,[2,3])
        v4 = Vertex(3,1,3,[4])
        v5 = Vertex(4,1,4,[3])
        v6 = Vertex(5,1,1,[5])
        g_not_c = Graph([v1,v2,v3,v4,v5,v6])
        self.assertEqual(g_not_c.nodeNetwork([3,4,5]),[3,4])
        self.assertEqual(g_not_c.nodeNetwork([0,1]),[0,1])
        self.assertEqual(g_not_c.nodeNetwork([2,4]),[2])

    def test_subCycles(self):
        # Test case 1: A simple cycle of length 3
        vertices = [Vertex(0, 0, 1, [1]), Vertex(1, 0, 1, [2]), Vertex(2, 0, 1, [0])]
        graph = Graph(vertices)
        cycles = graph.subCycles(3)
        self.assertEqual(cycles, [[0, 1, 2]])

        # Test case 2: A cycle of length 4 and a separate node
        vertices = [Vertex(0, 0, 1, [1]), Vertex(1, 0, 1, [2]), Vertex(2, 0, 1, [3]), Vertex(3, 0, 1, [0]), Vertex(4, 0, 1, [])]
        graph = Graph(vertices)
        cycles = graph.subCycles(4)
        self.assertEqual(cycles, [[0, 1, 2, 3]])

        # Test case 3: A cycle of length 3 and two separate nodes
        vertices = [Vertex(0, 0, 1, [1]), Vertex(1, 0, 1, [2]), Vertex(2, 0, 1, [0]), Vertex(3, 0, 1, []), Vertex(4, 0, 1, [])]
        graph = Graph(vertices)
        cycles = graph.subCycles(3)
        self.assertEqual(cycles, [[0, 1, 2]])

        # Test case 4: A disconnected graph with no cycles
        vertices = [Vertex(0, 0, 1, [1]), Vertex(1, 0, 1, []), Vertex(2, 0, 1, [3]), Vertex(3, 0, 1, [])]
        graph = Graph(vertices)
        cycles = graph.subCycles(3)
        self.assertEqual(cycles, [])

        # Test case 5: A cycle of length 2
        vertices = [Vertex(0, 0, 1, [1]), Vertex(1, 0, 1, [2]),Vertex(2, 0, 1, [0])]
        graph = Graph(vertices)
        cycles = graph.subCycles(2)
        self.assertEqual(cycles, [])
    
    def test_is_i_dominion(self):
        vertices = [Vertex(0, 0, 4, [1]), Vertex(1, 1, 3, [2,1,0]),Vertex(2, 0, 4, [0]),Vertex(3, 0, 1, [0])]
        graph = Graph(vertices)
        self.assertEqual(graph.is_i_dominion([0,1]),([False,False],[]))
        self.assertEqual(graph.is_i_dominion([0,1,2]),([False,True],[1]))
        vertices = [Vertex(0, 0, 4, [1]), Vertex(1, 1, 0, [2,1,0]),Vertex(2, 0, 4, [0]),Vertex(3, 0, 1, [0])]
        graph2 = Graph(vertices)
        self.assertEqual(graph2.is_i_dominion([0,1,2]),([True, False], [0, 1, 2]))
    
    def test_check_solution(self):

    # Create a graph with 6 vertices and 7 edges
        vertexList = [Vertex(0, 0, 1, [1]), Vertex(1, 1, 2, [2]), Vertex(2, 0, 3, [3]), 
                  Vertex(3, 1, 4, [4,0]), Vertex(4, 0, 5, [5]), Vertex(5, 1, 6, [0]), Vertex(6, 1, 7, [1])]
        graph = Graph(vertexList)

    # Check an invalid winning set
        solution = Graph([vertexList[0], vertexList[1], vertexList[2], vertexList[3], vertexList[4]])
        self.assertFalse(graph.checkSolution(solution, 0))

    # Check an invalid solution where not all nodes are in the graph
        solution = Graph([vertexList[0], vertexList[1], Vertex(7, 1, 1, [2])])
        self.assertFalse(graph.checkSolution(solution, 0))

        solution = solver_Iteration(Graph(self.vertices))[0]
        self.assertTrue(graph.checkSolution(solution, 0))


class TestSolverIteration(unittest.TestCase):
    def setUp(self):
        v1 = Vertex(0,0,2,[3])
        v2 = Vertex(1,0,3,[2,4])
        v3 = Vertex(2,0,2,[2,5])
        v4 = Vertex(3,1,3,[0,1])
        v5 = Vertex(4,1,4,[3,5])
        v6 = Vertex(5,1,1,[4,2])
        self.graph = Graph([v1,v2,v3,v4,v5,v6])
        self.graph_solution = [Graph([v2,v3]),Graph([v1,v4,v5,v6])]
    def test_solver_Iteration(self):
        result = solver_Iteration(self.graph)
        self.assertIsInstance(result[0], Graph)
        self.assertIsInstance(result[1], Graph)
        win0 = result[0].getIdList()
        self.assertEqual(win0, self.graph_solution[0].getIdList())

        # test if the winning set for player 1 is correct
        win1 = result[1].getIdList()
        self.assertEqual(win1, self.graph_solution[1].getIdList())
        
    def test_solver_Iteration_Dominion(self):
        result = solver_Dominion(self.graph)
        self.assertIsInstance(result[0], Graph)
        self.assertIsInstance(result[1], Graph)
        win0 = result[0].getIdList()
        self.assertEqual(win0, self.graph_solution[0].getIdList())
        win1 = result[1].getIdList()
        self.assertEqual(win1, self.graph_solution[1].getIdList())
       
        
if __name__ == '__main__':
    unittest.main()