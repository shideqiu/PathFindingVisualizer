import pygame
import math

from button import Button
from node import Node, GREY, WHITE
from algorithms import Algorithms

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


def draw(win, grid, rows, width, start_button, reset_button):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)

    start_button.draw(win)
    reset_button.draw(win)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
    algo = Algorithms(lambda: draw(win, grid, ROWS, width, start_button, reset_button),
                      grid, start_node, end_node)
    algo.astar()


def main(win, width=700):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start_node = None
    end_node = None

    run = True

    start_img = pygame.image.load('img/start.png').convert_alpha()
    reset_img = pygame.image.load('img/reset.png').convert_alpha()
    start_button = Button(200, 725, start_img, 1)
    reset_button = Button(400, 725, reset_img, 1)

    while run:
        draw(win, grid, ROWS, width, start_button, reset_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # press left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if start_button.rect.collidepoint(pos) and start_node and end_node:
                    start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node)
                elif reset_button.rect.collidepoint(pos):
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)
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
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None
            # press keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    start(win, grid, ROWS, width, start_button, reset_button, start_node, end_node)
                if event.key == pygame.K_c:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(WIN)
