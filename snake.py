# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:19:04 2020

@author: lucas
"""

# Snake AI

import pygame as pg
import random


# variáveis importantes
size_screen = (800, 600)    # tamanho da tela em pixels
blue = (0, 0, 255)          # cor azul
red = (255, 0, 0)           # cor vermelha
black = (0, 0, 0)           # cor preta
white = (255, 255, 255)     # cor branca
pos_inicial = (400, 300)    # posição inicial na tela
snake_block = 10            # tamanho do bloco da cabeça da cobra
snake_speed = 40            # velocidade da cobra
len_snake = 1               # tamanho da cobra
x_change = 0                # necessário para fazer o deslocamento da cobra
y_change = 0                # necessário para fazer o deslocamento da cobra
food_block = 10             # tamanho do bloco da comida

pos_snake = [pos_inicial]
x0, y0 = pos_inicial
x_max_screen, y_max_screen= size_screen
pg.init()
dis = pg.display.set_mode(size_screen)
clock = pg.time.Clock()
pg.display.set_caption("Snake-AI by Lucas Garcia")

game_over = False

font_style = pg.font.SysFont(None, 50)

def message(msg, color, dis):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, (dis.get_width()/2, dis.get_height()/2))
    
def show_score(score, color, dis):
    score_board = font_style.render("Score: " + str(score), True, color)
    dis.blit(score_board, (0, 0))
    
def grows_snake(pos_snake, new_pos, len_snake):
    pos_snake.append(pos_snake[len_snake-1])
    for i in reversed(range(len_snake)):
        pos_snake[i] = pos_snake[i-1]
    pos_snake[0] = new_pos
    len_snake += 1
    
    return pos_snake, len_snake
    
def move_snake(pos_snake, new_pos, len_snake):
    for i in reversed(range(len_snake)):
        if i != 0:
            pos_snake[i] = pos_snake[i-1]
    pos_snake[0] = new_pos
        
    return pos_snake

def self_eat(pos_snake):
    if pos_snake[0] in pos_snake[1:]:
        return True
    else: 
        return False

def draw_snake(pos_snake, dis):
    for i in pos_snake:
        x, y = i
        pg.draw.rect(dis, blue, (x, y, snake_block, snake_block))
    
def place_food(dis):
    y_food = random.randrange(0, dis.get_height(), 10)
    x_food = random.randrange(0, dis.get_width(), 10)
    
    return x_food, y_food

# Iniciando um lugar aleatório para a comida
x_food, y_food = place_food(dis)

# Score 0
score = 0
    
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        if event.type == pg.KEYDOWN:    # controla a movimentação da cobra
            if event.key == pg.K_LEFT:
                x_change = -snake_block
                y_change = 0
            elif event.key == pg.K_RIGHT:
                x_change = snake_block
                y_change = 0
            elif event.key == pg.K_UP:
                x_change = 0
                y_change = -snake_block
            elif event.key == pg.K_DOWN:
                x_change = 0
                y_change = snake_block
                
            x0 += x_change
            y0 += y_change
        
            if x0 == x_food and y0 == y_food:    # comeu a comida
                score += 100
                x_food, y_food = place_food(dis)
                pos_snake, len_snake = grows_snake(pos_snake, (x0, y0), len_snake)
            else:                                # só se movimentou
                pos_snake = move_snake(pos_snake, (x0, y0), len_snake)
                score -= 1
                print(pos_snake)
            
            if x0 >= x_max_screen or x0 <= 0 or y0 >= y_max_screen or y0 <= 0: # verifica se a cobra bateu na borda 
                game_over = True
            else:
                game_over = self_eat(pos_snake)
            
        
        dis.fill(white)
        
        draw_snake(pos_snake, dis)
        show_score(score, blue, dis)
        pg.draw.rect(dis, red, (x_food, y_food, food_block, food_block))
        pg.display.update()

        clock.tick(snake_speed)
        
message("You Lost", blue, dis)
pg.display.update()
#time.sleep(2)

pg.quit()
quit()