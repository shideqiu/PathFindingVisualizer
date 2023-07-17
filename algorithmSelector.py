import pygame
from pygame.locals import *
from node import BLACK, WHITE, GREY

pygame.init()
font = pygame.font.SysFont('Constantia', 20)


class AlgorithmSelector:
    # colours for button and text
    button_col = (10,10,35)
    hover_col = (0,46,173)
    click_col = (50, 150, 255)
    text_col = WHITE
    width = 100
    height = 50

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw_button(self, win):

        clicked = False
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            # if pygame.mouse.get_pressed()[0] == 1:
            #     clicked = True
            #     selected = True
            #     pygame.draw.rect(win, self.click_col, self.rect)
            # elif pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            #     clicked = False
            #     action = True
            # else:
            pygame.draw.rect(win, self.hover_col, self.rect)
        else:
            pygame.draw.rect(win, self.button_col, self.rect)

        # add shading to button
        pygame.draw.line(win, GREY, (self.x, self.y), (self.x + self.width, self.y), 3)
        pygame.draw.line(win, GREY, (self.x, self.y), (self.x, self.y + self.height), 3)
        pygame.draw.line(win, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(win, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        win.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action

    def draw_selected(self, win, selected):
        if selected:
            pygame.draw.rect(win, self.click_col, self.rect)
            text_img = font.render(self.text, True, self.text_col)
            text_len = text_img.get_width()
            win.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))