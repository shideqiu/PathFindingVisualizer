from queue import PriorityQueue

import pygame



def manhattan_distance_heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def euclidean_distance_heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Algorithms:
    def __init__(self, draw, grid, start_node, end_node):
        self.draw = draw
        self.grid = grid
        self.start_node = start_node
        self.end_node = end_node

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw()

    def astar(self):
        """
        Warm-up exercise: Implement A* algorithm.

        See README.md for exercise description.

        Args:
            graph (ExplorableGraph): Undirected graph to search.
            start (str): Key for the start node.
            goal (str): Key for the end node.
            heuristic: Function to determine distance heuristic.
                Default: euclidean_dist_heuristic.

        Returns:
            The best path as a list from the start and goal nodes (including both).
        """
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start_node))
        came_from = {}
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[self.start_node] = 0
        f_score = {node: float("inf") for row in self.grid for node in row}
        f_score[self.start_node] = manhattan_distance_heuristic(self.start_node.get_pos(), self.end_node.get_pos())

        open_set_hash = {self.start_node}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end_node:
                self.reconstruct_path(came_from, self.end_node)
                self.end_node.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + manhattan_distance_heuristic(neighbor.get_pos(),
                                                                                    self.end_node.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            self.draw()
            if current != self.start_node:
                current.make_closed()
        return False
