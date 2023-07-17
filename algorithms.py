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

    def bi_ucs(self):
        path = self.bi_ucs_helper()
        path.remove(self.start_node)
        path.remove(self.end_node)
        steps = 1
        for current in path:
            steps += 1
            current.make_path()
        self.draw()
        return steps

    def bi_ucs_helper(self):
        """
        Bidirectional Search.
    
        Returns:
            The best path as a list from the start and goal nodes (including both).
        """
        frontier = PriorityQueue()
        frontier.append((0, self.start_node))
        back_frontier = PriorityQueue()
        back_frontier.append((0, self.end_node))
        path = {self.start_node: [self.start_node]}
        back_path = {self.end_node: [self.end_node]}
        explored = set()
        back_explored = set()
    
        while frontier and back_frontier:
            node = frontier.pop()
            back_node = back_frontier.pop()
            best_crossover = (0, float('inf'))
            if node[-1] == back_node[-1]:
                temp = node[0] + back_node[0]
                """Use for loop to check the crossover.
                a list of potential crossover points can be made from all start_explored set nodes that are
                also found in the union of the goal_frontier and the goal_explored nodes.
                For each crossover point, we should check if the path cost from start to that point + the path
                cost from goal to that point exceeds the lowest cost path we have found so far (which is initialized
                to infinity. If it is, then that point becomes the lowest cost point."""
                for explored_node in explored:
                    if frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
                    elif back_frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + back_frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
    
                if best_crossover[1] < temp:
                    return path[best_crossover[0]] + list(reversed(back_path[best_crossover[0]]))[1:]
                else:
                    return path[node[-1]] + list(reversed(back_path[node[-1]]))[1:]
    
            if node[-1] in [element[-1] for element in back_explored]:
                temp = node[0] + list(filter(lambda x: node[-1] in x, back_explored))[0][0]
            else:
                temp = float('inf')
            if back_node[-1] in [element[-1] for element in explored]:
                back_temp = back_node[0] + list(filter(lambda x: back_node[-1] in x, explored))[0][0]
            else:
                back_temp = float('inf')
    
            if temp > back_temp:
                for explored_node in explored:
                    if frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
                    elif back_frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + back_frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
    
                if best_crossover[1] < back_temp:
                    return path[best_crossover[0]] + list(reversed(back_path[best_crossover[0]]))[1:]
                else:
                    return path[back_node[-1]] + list(reversed(back_path[back_node[-1]]))[1:]
            elif temp < back_temp:
                for explored_node in explored:
                    if frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
                    elif back_frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + back_frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
    
                if best_crossover[1] < temp:
                    return path[best_crossover[0]] + list(reversed(back_path[best_crossover[0]]))[1:]
                else:
                    return path[node[-1]] + list(reversed(back_path[node[-1]]))[1:]
            elif (temp == back_temp) and (temp < float('inf')):
                for explored_node in explored:
                    if frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
                    elif back_frontier.__contains__(explored_node[-1]):
                        crossover = explored_node[0] + back_frontier.get(explored_node[-1])
                        if crossover < best_crossover[1]:
                            best_crossover = (explored_node[-1], crossover)
    
                if best_crossover[1] < temp:
                    return path[best_crossover[0]] + list(reversed(back_path[best_crossover[0]]))[1:]
                else:
                    return path[node[-1]] + list(reversed(back_path[node[-1]]))[1:]
    
            explored.add(node)
            back_explored.add(back_node)
            for child_node in node[-1].neighbors:
                if child_node not in [element[-1] for element in explored] and not frontier.__contains__(child_node):
                    frontier.append((1 + node[0], child_node))
                    path[child_node] = path[node[-1]] + [child_node]
                    child_node.make_open()
    
                elif frontier.__contains__(child_node):
                    if frontier.remove((1 + node[0], child_node)):
                        path[child_node] = path[node[-1]] + [child_node]
    
            for child_node in back_node[-1].neighbors:
                if child_node not in [element[-1] for element in back_explored] and not back_frontier.__contains__(child_node):
                    back_frontier.append((1 + back_node[0], child_node))
                    back_path[child_node] = back_path[back_node[-1]] + [child_node]
                    child_node.make_open()
    
                elif back_frontier.__contains__(child_node):
                    if back_frontier.remove((1 + back_node[0], child_node)):
                        back_path[child_node] = back_path[back_node[-1]] + [child_node]
            self.draw()
            if node[-1] != self.start_node and node[-1] != self.end_node:
                node[-1].make_closed()
            if back_node[-1] != self.start_node and back_node[1] != self.end_node:
                back_node[-1].make_closed()
        return False