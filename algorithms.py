from priorityQueue import PriorityQueue
from queue import PriorityQueue as pq
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
        """
        Args:
            draw: function to draw the path.
            grid (nodes): grid of nodes
            start_node: start node.
            end_node: end node.
        """
        self.draw = draw
        self.grid = grid
        self.start_node = start_node
        self.end_node = end_node

    def reconstruct_path(self, path, current):
        """
        Implement the optimal path construction.

        Returns:
            The total steps of the optimal path
        """
        steps = 0
        while current in path:
            steps += 1
            current = path[current]
            if current == self.start_node:
                return steps
            current.make_path()
            self.draw()

    def bfs(self):
        """
        Implement breadth-first-search.

        Returns:
            The best path as a dictionary from the start and goal nodes (including both).
        """
        frontier = [(0, self.start_node)]
        path = {self.start_node: self.start_node}
        explored = set()
        n = 0
        while frontier:
            frontier = sorted(frontier)
            node = frontier.pop(0)
            if node[-1] == self.end_node:
                steps = self.reconstruct_path(path, self.end_node)
                self.end_node.make_end()
                return steps
            explored.add(node[-1])
            n += 1
            for child_node in node[-1].neighbors:
                if child_node not in explored and child_node not in [n[-1] for n in frontier]:
                    path[child_node] = node[-1]
                    child_node.make_open()
                    frontier.append((n, child_node))
            self.draw()
            if node[-1] != self.start_node:
                node[-1].make_closed()
        return False

    def greedy(self):
        """
        Implement greedy search.

        Returns:
            The best path as a dictionary from the start and goal nodes (including both).
        """
        frontier = PriorityQueue()
        frontier.append((manhattan_distance_heuristic(self.start_node.get_pos(), self.end_node.get_pos()),
                         self.start_node))
        path = {self.start_node: self.start_node}
        explored = set()
        while frontier:
            node = frontier.pop()
            if node[-1] == self.end_node:
                steps = self.reconstruct_path(path, self.end_node)
                self.end_node.make_end()
                return steps
            explored.add(node[-1])
            for child_node in node[-1].neighbors:
                if child_node not in explored and not frontier.__contains__(child_node):
                    frontier.append((manhattan_distance_heuristic(child_node.get_pos(), self.end_node.get_pos()),
                                     child_node))
                    path[child_node] = node[-1]
                    child_node.make_open()
                elif frontier.__contains__(child_node):
                    if frontier.remove((manhattan_distance_heuristic(child_node.get_pos(), self.end_node.get_pos()),
                                        child_node)):
                        path[child_node] = node[-1]
            self.draw()
            if node[-1] != self.start_node:
                node[-1].make_closed()
        return False

    def astar(self):
        """
        Implement astar search.

        Returns:
            The best path as a dictionary from the start and goal nodes (including both).
        """
        frontier = PriorityQueue()
        frontier.append((manhattan_distance_heuristic(self.start_node.get_pos(), self.end_node.get_pos()),
                         self.start_node))
        path = {self.start_node: self.start_node}
        explored = set()
        while frontier:
            node = frontier.pop()
            if node[-1] == self.end_node:
                steps = self.reconstruct_path(path, self.end_node)
                self.end_node.make_end()
                return steps
            explored.add(node[-1])
            for child_node in node[-1].neighbors:
                if child_node not in explored and not frontier.__contains__(child_node):
                    frontier.append((1 + node[0] +
                                     manhattan_distance_heuristic(child_node.get_pos(), self.end_node.get_pos()) -
                                     manhattan_distance_heuristic(node[-1].get_pos(), self.end_node.get_pos()),
                                     child_node))
                    path[child_node] = node[-1]
                    child_node.make_open()
                elif frontier.__contains__(child_node):
                    if frontier.remove((1 + node[0] +
                                        manhattan_distance_heuristic(child_node.get_pos(), self.end_node.get_pos()) -
                                        manhattan_distance_heuristic(node[-1].get_pos(), self.end_node.get_pos()),
                                        child_node)):
                        path[child_node] = node[-1]
            self.draw()
            if node[-1] != self.start_node:
                node[-1].make_closed()
        return False

