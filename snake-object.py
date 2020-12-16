# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:19:04 2020

@author: lucas
"""

# Snake AI - Orientado a objeto

import pygame as pg
import random

class Snake:
    
    def __init__(self, color, dim_display):
        self.x_max, self.y_max = dim_display
        self.pos_snake = [(self.x_max/2, self.y_max/2)]
        self.x_head, self.y_head = self.pos_snake[0]
        self.color = color
        self.last_direction = "nothing"    
        
    def move(self, direction, food): # Retorna se o jogo acaba ou não
        
        #------------Posiciona a cabeça da cobra------------#
        if self.lenght > 1:
            if self.last_direction == "right" and direction == "left":
                return False
            elif self.last_direction == "left" and direction == "right":
                return False
            elif self.last_direction == "up" and direction == "down":
                return False
            elif self.last_direction == "down" and direction == "up":
                return False
            else:
                self.last_direction = direction
            
        if direction == "right":
            self.x_head += self.block_size
        elif direction == "left":
            self.x_head -= self.block_size
        elif direction == "up":
            self.y_head -= self.block_size
        else:
            self.y_head += self.block_size
            
        new_pos = (self.x_head, self.y_head)
        
        #------------Verifica se ela não vai se comer------------#
        
        if new_pos in self.pos_snake:
            return True
        
        #------------Verifica se ela não vai bater na borda------------#
        
        if self.x_head >= self.x_max or self.x_head < 0 or self.y_head >= self.y_max or self.y_head < 0:
            return True
        
        #------------Se ela poder se mover, então verifica se ela comeu------------#
        
        food_place = (food.pos_x, food.pos_y)
        if new_pos == food_place:
            self.pos_snake.append(self.pos_snake[self.lenght-1])
            for i in reversed(range(self.lenght)):
                self.pos_snake[i] = self.pos_snake[i-1]
            self.pos_snake[0] = new_pos
            self.lenght += 1
            food.place_food()
        else:
            for i in reversed(range(self.lenght)):
                if i != 0:
                    self.pos_snake[i] = self.pos_snake[i-1]
            self.pos_snake[0] = (new_pos)
            
        self.dist_borda()
        
        return False
    
    def dist_borda(self):
        self.leste_borda = self.x_max - self.x_head
        self.norte_borda = self.y_head
        self.oeste_borda = self.x_head
        self.sul_borda = self.y_max - self.y_head
        
        if self.leste_borda <= self.norte_borda:
            self.nordeste_borda = int(1.4142 * self.leste_borda)
        else:
            self.nordeste_borda = int(1.4142 * self.norte_borda)
            
        if self.norte_borda <= self.oeste_borda:
            self.noroeste_borda = int(1.4142 * self.norte_borda)
        else:
            self.noroeste_borda = int(1.4142 * self.oeste_borda)
            
        if self.oeste_borda <= self.sul_borda:
            self.sudoeste_borda = int(1.4142 * self.oeste_borda)
        else:
            self.sudoeste_borda = int(1.4142 * self.sul_borda)
        
        if self.sul_borda <= self.leste_borda:
            self.sudeste_borda = int(1.4142 * self.sul_borda)
        else:
            self.sudeste_borda = int(1.4142 * self.leste_borda)
            
    def dist_self(self): # por enquanto só tem distância em quatro direções
        # verificando se ao norte tem corpo dela
        for i in range(0, self.y_head, 10):
            if (self.x_head, i) in self.pos_snake:
                self.norte_self = self.y_head - i
                break
            else:
                self.norte_self = None
        
        # verificando se ao leste tem corpo dela
        for i in range(self.x_head + 10, self.x_max, 10):
            if (i, self.y_head) in self.pos_snake:
                self.leste_self = i - self.x_head
                break
            else:
                self.leste_self = None
                
        # verificando se ao sul tem corpo dela
        for i in range(self.y_head + 10, self.y_max, 10):
            if(self.x_head, i) in self.pos_snake:
                self.sul_self = i - self.y_head
                break
            else:
                self.sul_self = None
                
        # verificando se a oeste tem corpo dela
        for i in range(0, self.x_head, 10):
            if(i, self.y_head) in self.pos_snake:
                self.oeste_self = self.x_head - i
                break
            else:
                self.oeste_self = None
                
    #def dist_food(self, pos_food):
        
                
        
        
        
    block_size = 10
    lenght = 1
    speed = 40
    
    #------------Sensores------------#
    
    #------------Distância bordas------------#
    leste_borda = None
    nordeste_borda = None
    norte_borda = None
    noroeste_borda = None
    oeste_borda = None
    sudoeste_borda = None
    sul_borda = None
    sudeste_borda = None
    
    #------------Distância dela mesma------------#
    leste_self = None
    norte_self = None
    oeste_self = None
    sul_self = None
    
    #------------Distância da comida------------#
    dist_food_abs = None
    dist_food_graus = None
    
class Food:
    def __init__(self, color, dim_display):
        self.x_max, self.y_max = dim_display
        self.color = color
        self.pos_x = random.randrange(0, self.x_max, 10)
        self.pos_y = random.randrange(0, self.y_max, 10)
        
    def place_food(self):
        self.pos_x = random.randrange(0, self.x_max, 10)
        self.pos_y = random.randrange(0, self.y_max, 10)
        
    block_size = 10
    

# variáveis importantes
size_screen = (800, 600)    # tamanho da tela em pixels
blue = (0, 0, 255)          # cor azul
red = (255, 0, 0)           # cor vermelha
black = (0, 0, 0)           # cor preta
white = (255, 255, 255)     # cor branca

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
    

def draw_snake(snake, dis):
    for i in snake.pos_snake:
        x, y = i
        pg.draw.rect(dis, blue, (x, y, snake.block_size, snake.block_size))

# Score 0
score = 0

snake1 = Snake(blue, dis.get_size())
food = Food(red, dis.get_size())

while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        if event.type == pg.KEYDOWN:    # controla a movimentação da cobra
            if event.key == pg.K_LEFT:
                game_over = snake1.move("left", food)
            elif event.key == pg.K_RIGHT:
                game_over = snake1.move("right", food)
            elif event.key == pg.K_UP:
                game_over = snake1.move("up", food)
            elif event.key == pg.K_DOWN:
                game_over = snake1.move("down", food)
                
        dis.fill(white)
        
        
        draw_snake(snake1, dis)
        show_score(snake1.norte_borda, blue, dis)
        pg.draw.rect(dis, red, (food.pos_x, food.pos_y, food.block_size, food.block_size))
        pg.display.update()

        clock.tick(snake1.speed)
        
message("You Lost", blue, dis)
pg.display.update()
#time.sleep(2)

pg.quit()
quit()