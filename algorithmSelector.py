import pygame
from pygame.locals import *
from node import BLACK, WHITE, RED

pygame.init()
font = pygame.font.SysFont('Constantia', 20)


class AlgorithmSelector:
    # colours for button and text
    button_col = RED
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = BLACK
    width = 100
    height = 50

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self, win):

        clicked = False
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(win, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(win, self.hover_col, button_rect)
        else:
            pygame.draw.rect(win, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(win, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(win, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(win, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(win, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        win.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action
