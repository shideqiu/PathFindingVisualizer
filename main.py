import pygame
import math

from algorithmSelector import AlgorithmSelector
from button import Button
from node import Node, GREY, WHITE, BLACK
from algorithms import Algorithms
from algorithmSelector import font

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows + 1):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, start_button, reset_button, algorithms, selected_algorithm=None):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)

    start_button.draw(win)
    reset_button.draw(win)

    text = font.render("Search Algorithms", True, BLACK)
    win.blit(text, (625, 50))

    for algo in algorithms:
        algo.draw_button(win)
    if selected_algorithm:
        # algorithms.remove(selected_algorithm)
        selected_algorithm.draw_selected(win, True)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node, algorithms, selected):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
    algo = Algorithms(lambda: draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected),
                      grid, start_node, end_node)
    algo.astar()


def main(win, width=600):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start_node = None
    end_node = None

    run = True

    start_img = pygame.image.load('img/start.png').convert_alpha()
    reset_img = pygame.image.load('img/reset.png').convert_alpha()
    start_button = Button(150, 650, start_img, 1)
    reset_button = Button(350, 650, reset_img, 1)

    bfs = AlgorithmSelector(650, 100, 'BFS')
    ucs = AlgorithmSelector(650, 175, 'UCS')
    astar = AlgorithmSelector(650, 250, 'A-Star')
    bi_ucs = AlgorithmSelector(650, 325, 'BiUCS')
    bi_astar = AlgorithmSelector(650, 400, 'BI A-Star')

    algorithms = [bfs, ucs, astar, bi_ucs, bi_astar]
    selected = bfs
    while run:
        draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # press left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if start_button.rect.collidepoint(pos) and start_node and end_node:
                    start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node, algorithms, selected)
                elif reset_button.rect.collidepoint(pos):
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)

                elif bfs.rect.collidepoint(pos):
                    selected = bfs
                    draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)
                elif ucs.rect.collidepoint(pos):
                    selected = ucs
                    draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)
                elif astar.rect.collidepoint(pos):
                    selected = astar
                    draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)
                elif bi_ucs.rect.collidepoint(pos):
                    selected = bi_ucs
                    draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)
                elif bi_astar.rect.collidepoint(pos):
                    selected = bi_astar
                    draw(win, grid, ROWS, width, start_button, reset_button, algorithms, selected)

                elif row < ROWS and col < ROWS:
                    node = grid[row][col]
                    if not start_node and node != end_node:
                        start_node = node
                        start_node.make_start()
                    elif not end_node and node != start_node:
                        end_node = node
                        end_node.make_end()
                    elif node != start_node and node != end_node:
                        node.make_barrier()

            # press right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if row < ROWS and col < ROWS:
                    node = grid[row][col]
                    node.reset()
                    if node == start_node:
                        start_node = None
                    elif node == end_node:
                        end_node = None
            # press keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node, algorithms, selected)
                if event.key == pygame.K_c:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


if __name__ == "__main__":
    main(WIN)
