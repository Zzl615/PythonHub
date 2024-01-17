from typing import List


class GraphAdjMatrix:

    """
        Graph represented by adjacency matrix.
    """

    vertices: List[int]
    edges: List[List[int]]

    def __init__(self, vertices: List[int], edges: List[List[int]]):
        self.vertices = vertices
        self.edges = [[0] * len(vertices) for _ in range(len(vertices))]
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

    
    def check_vertex(self, from_vertex: int, to_vertex: int):
        """
            Check Whether vertex exists. If exists, return index.
        """
        from_index, to_index = None, None
        for index, vertex in enumerate(self.vertices):
            if vertex == from_vertex:
                from_index = index
            if vertex == to_vertex:
                to_index = index
        if from_index is None or to_index is None:
            raise Exception("Vertex not found")
        return from_index, to_index  

    def add_edge(self, from_vertex: int, to_vertex: int, weight: int = 1):
        """
            Add edge from from_vertex to to_vertex.
        """
        from_index, to_index = self.check_vertex(from_vertex, to_vertex)
        # 无向图，矩阵对称
        self.edges[from_index][to_index] = weight
        self.edges[to_index][from_index] = weight

    
    def remove_edge(self, from_vertex: int, to_vertex: int):
        """
            Remove edge from from_vertex to to_vertex.
        """
        from_index, to_index = self.check_vertex(from_vertex, to_vertex)
        # 无向图，矩阵对称
        self.edges[from_index][to_index] = 0
        self.edges[to_index][from_index] = 0

    def add_vertex(self, vertex: int):
        """
            Add vertex to graph.
        """
        self.vertices.append(vertex)
        # 矩阵扩展
        ## 行扩展
        for edge in self.edges:
            edge.append(0)
        ## 新增列
        self.edges.append([0] * len(self.vertices))

    def remove_vertex(self, vertex: int):
        """
            Remove vertex from graph.
        """
        vertex_index = None
        for index, v in enumerate(self.vertices):
            if v == vertex:
                vertex_index = index
                break
        if vertex_index is None:
            raise Exception("Vertex not found")
        # 删除顶点
        self.vertices.pop(vertex_index)
        # 删除边
        self.edges.pop(vertex_index)
        for edge in self.edges:
            edge.pop(vertex_index)

    
    @property
    def vertex_count(self):
        return len(self.vertices)
    
    @property
    def edge_count(self):
        count = 0
        for edge in self.edges:
            count += sum(edge)
        return count // 2
    
    def __str__(self):
        """Print graph representation."""
        result = ""
        for index, vertex in enumerate(self.vertices):
            result += f"{vertex}: "
            for edge in self.edges[index]:
                result += f"{edge} "
            result += "\n"
        return result


def test_gragh_adjmet():
    vertices = [1, 2, 3, 4, 5]
    edges = [
        [1, 2, 1],
        [1, 3, 1],
        [1, 4, 1],
        [2, 3, 1],
        [3, 4, 1],
        [4, 5, 1]
    ]
    graph = GraphAdjMatrix(vertices, edges)
    print(f"Vertex count: {graph.vertex_count}")
    print(f"Edge count: {graph.edge_count}")
    print(graph)
    graph.add_vertex(6)
    print(graph)
    graph.add_edge(1, 6, 6)
    print(graph)
    graph.remove_edge(1, 6)
    print(graph)
    graph.remove_vertex(6)
    print(graph)

if __name__ == "__main__":
    test_gragh_adjmet()
    
            