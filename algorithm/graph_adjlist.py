from typing import List, Dict

class GraphAdjList:
    
    adj_map: Dict[int, List[int]]

    def __init__(self, edges: List[List[int]]):
        self.adj_map = {}
        for edge in edges:
            self.add_edge(edge[0], edge[1])

    def add_edge(self, from_vertex: int, to_vertex: int):
        if from_vertex not in self.adj_map:
            self.adj_map[from_vertex] = []
        if to_vertex not in self.adj_map:
            self.adj_map[to_vertex] = []
        self.adj_map[from_vertex].append(to_vertex)
        self.adj_map[to_vertex].append(from_vertex)

    def remove_edge(self, from_vertex: int, to_vertex: int):
        if from_vertex not in self.adj_map or to_vertex not in self.adj_map:
            raise Exception("Vertex not found")
        self.adj_map[from_vertex].remove(to_vertex)
        self.adj_map[to_vertex].remove(from_vertex)

    def add_vertex(self, vertex: int):
        if vertex not in self.adj_map:
            self.adj_map[vertex] = []

    def remove_vertex(self, vertex: int):
        if vertex not in self.adj_map:
            raise Exception("Vertex not found")
        for other_vertex in self.adj_map:
            if vertex in self.adj_map[other_vertex]:
                self.adj_map[other_vertex].remove(vertex)
        del self.adj_map[vertex]

    @property
    def vertex_count(self):
        return len(self.adj_map)
    
    @property
    def edge_count(self):
        count = 0
        for vertex in self.adj_map:
            count += len(self.adj_map[vertex])
        return count // 2

def test_gragh_adjlist():
    graph = GraphAdjList([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]])
    assert graph.vertex_count == 4
    assert graph.edge_count == 5
    print(graph.adj_map)
    graph.remove_edge(1, 2)
    assert graph.edge_count == 4
    print(graph.adj_map)
    graph.remove_vertex(1)
    print(graph.adj_map)
    assert graph.vertex_count == 3
    assert graph.edge_count == 2
    print(graph.adj_map)

if __name__ == "__main__":
    test_gragh_adjlist()