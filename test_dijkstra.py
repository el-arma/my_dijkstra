import unittest
from pathfinders import dijkstra_algo  


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        # Define a sample graph for testing
        self.graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }
        self.start = 'A'
        self.goal = 'D'

    def test_dijkstra(self):
        expected_path = ['A', 'B', 'C', 'D']
        expected_cost = 4
        path, cost = dijkstra_algo(self.graph, self.start, self.goal)
        self.assertEqual(path, expected_path)
        self.assertEqual(cost, expected_cost)

if __name__ == '__main__':
    unittest.main()
